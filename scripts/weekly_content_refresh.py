#!/usr/bin/env python3
"""Generate a weekly zemna.net content refresh report.

This script combines:
- local post metadata and editorial QA signals
- optional live GSC/GA4 summary from ~/.hermes/scripts/zemnanet_seo_report.py
- a prioritized refresh queue for existing posts

It writes a markdown artifact into the local LLM Wiki so future blog/social crons
can use the findings.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "content" / "posts"
WIKI = Path.home() / "wiki" / "default" / "concepts"
OUTPUT = WIKI / "weekly-content-refresh-latest.md"
JSON_OUTPUT = WIKI / "weekly-content-refresh-latest.json"
SEO_REPORTER = Path.home() / ".hermes" / "scripts" / "zemnanet_seo_report.py"


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    _, fm, body = text.split("---", 2)
    return fm, body


def line_value(frontmatter: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", frontmatter, re.M)
    return match.group(1).strip().strip('"') if match else ""


def array_values(raw: str) -> list[str]:
    return re.findall(r'"([^"]+)"', raw)


def slugify_title(title: str) -> str:
    slug = title.lower()
    slug = slug.replace("—", "-").replace("–", "-")
    slug = re.sub(r"[^a-z0-9.]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def post_url(frontmatter: str, path: Path) -> str:
    explicit_url = line_value(frontmatter, "url")
    if explicit_url:
        return "https://zemna.net" + explicit_url if explicit_url.startswith("/") else explicit_url
    title = line_value(frontmatter, "title")
    # Prefer the built Hugo URL when public/ exists. This avoids mismatches around
    # punctuation such as don't/doesn't/Here's.
    public_blog = ROOT / "public" / "blog"
    if public_blog.exists() and title:
        for index in public_blog.glob("*/index.html"):
            html = index.read_text(errors="replace")
            match = re.search(r"<title>(.*?)</title>", html, re.S)
            page_title = re.sub(r"<.*?>", "", match.group(1)).replace(" — zemnanet", "").strip() if match else ""
            if page_title == title:
                return "https://zemna.net/" + str(index.parent.relative_to(ROOT / "public")) + "/"
    slug = line_value(frontmatter, "slug")
    final_slug = slug or slugify_title(title) or path.stem
    return f"https://zemna.net/blog/{final_slug}/"


def collect_posts() -> list[dict[str, object]]:
    rows = []
    for path in sorted(POSTS.glob("*.md")):
        if path.name == "_index.md" or path.name.startswith("fact-check"):
            continue
        text = path.read_text(errors="replace")
        fm, body = split_frontmatter(text)
        if not fm or line_value(fm, "draft").lower() == "true":
            continue
        title = line_value(fm, "title")
        date_raw = line_value(fm, "date")
        topics = array_values(line_value(fm, "topics"))
        seo_primary = ""
        primary_match = re.search(r"primaryQuery:\s*\"([^\"]+)\"", fm)
        if primary_match:
            seo_primary = primary_match.group(1)
        words = len(re.findall(r"\b\w+\b", body))
        rows.append({
            "file": str(path.relative_to(ROOT)),
            "url": post_url(fm, path),
            "title": title,
            "date": date_raw[:10],
            "topics": topics,
            "seoPrimary": seo_primary,
            "words": words,
            "hasFieldNote": "{{< field-note" in body,
            "hasMondayAction": bool(re.search(r"^## What you should do Monday morning\b", body, re.M | re.I)),
            "hasRefreshNote": "## Refresh note" in body,
        })
    return rows


def run_seo_report() -> str:
    if not SEO_REPORTER.exists():
        return "SEO reporter not found. Local refresh queue only."
    proc = subprocess.run(
        ["python3", str(SEO_REPORTER)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=180,
    )
    if proc.returncode != 0:
        return "SEO reporter failed:\n\n```text\n" + (proc.stdout + proc.stderr)[-4000:] + "\n```"
    return proc.stdout.strip()


def score_post(row: dict[str, object]) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    words = int(str(row["words"]))
    if words < 1500:
        score += 2
        reasons.append("shorter than 1,500 words")
    if not row["hasRefreshNote"]:
        score += 2
        reasons.append("no refresh note yet")
    if not row["hasFieldNote"]:
        score += 3
        reasons.append("missing field note")
    if not row["hasMondayAction"]:
        score += 3
        reasons.append("missing Monday action")
    if not row["seoPrimary"]:
        score += 3
        reasons.append("missing primary SEO query")
    return score, reasons


def build_report(posts: list[dict[str, object]], seo_text: str) -> tuple[str, dict[str, object]]:
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=7)))
    scored = []
    for row in posts:
        score, reasons = score_post(row)
        scored.append({**row, "refreshScore": score, "reasons": reasons})
    queue = sorted(scored, key=lambda r: (-int(r["refreshScore"]), str(r["date"])))[:12]

    lines = [
        "# Weekly Content Refresh Report",
        "",
        f"Generated: {now.strftime('%Y-%m-%d %H:%M WIB')}",
        "",
        "## SEO / analytics readback",
        "",
        seo_text if seo_text else "No SEO reporter output.",
        "",
        "## Refresh queue",
        "",
        "| Priority | Post | Primary query | Reason |",
        "|---:|---|---|---|",
    ]
    for row in queue:
        reasons = "; ".join(row["reasons"]) or "watch analytics movement"
        lines.append(
            f"| {row['refreshScore']} | [{row['title']}]({row['url']}) | {row['seoPrimary']} | {reasons} |"
        )
    lines += [
        "",
        "## Editorial operating rules",
        "",
        "- Refresh pages with GSC impressions before creating another near-duplicate post.",
        "- Every refreshed post must keep a field note, a Monday action, and at least three internal links.",
        "- Promote pages that move in GSC after 14, 28, and 56 days. Mark weak changes as unproven.",
        "- Feed the top three opportunities into the next Blog Daily Post and social scheduling briefs.",
    ]
    data = {"generatedAtWib": now.isoformat(), "postCount": len(posts), "queue": queue}
    return "\n".join(lines).strip() + "\n", data


def main() -> int:
    WIKI.mkdir(parents=True, exist_ok=True)
    posts = collect_posts()
    seo_text = run_seo_report()
    report, data = build_report(posts, seo_text)
    OUTPUT.write_text(report)
    JSON_OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
