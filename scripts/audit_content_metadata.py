#!/usr/bin/env python3
"""Audit zemna.net post frontmatter for professional publishing quality."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "content" / "posts"


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return "", text
    return parts[1], parts[2]


def line_value(frontmatter: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", frontmatter, re.M)
    return m.group(1).strip() if m else ""


def array_values(raw: str) -> list[str]:
    return re.findall(r'"([^"]+)"', raw)


def is_public_post(frontmatter: str) -> bool:
    draft = line_value(frontmatter, "draft").lower()
    if draft == "true":
        return False
    if "_build:" in frontmatter and re.search(r"render:\s*never", frontmatter):
        return False
    return True


def audit() -> list[str]:
    issues: list[str] = []
    for path in sorted(POSTS.glob("*.md")):
        if path.name == "_index.md":
            continue
        frontmatter, body = split_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        if not frontmatter:
            issues.append(f"{path.name}: missing frontmatter")
            continue
        if not is_public_post(frontmatter):
            continue

        title = line_value(frontmatter, "title").strip('"')
        description = line_value(frontmatter, "description").strip('"')
        cover = line_value(frontmatter, "cover").strip('"')
        topics = array_values(line_value(frontmatter, "topics"))
        tags = array_values(line_value(frontmatter, "tags"))

        if not title:
            issues.append(f"{path.name}: missing title")
        if not description:
            issues.append(f"{path.name}: missing description")
        elif not (70 <= len(description) <= 240):
            issues.append(f"{path.name}: description length {len(description)} should be 70-240 chars")
        if not cover:
            issues.append(f"{path.name}: missing cover")
        else:
            cover_path = ROOT / "static" / cover.lstrip("/")
            if not cover_path.exists():
                issues.append(f"{path.name}: cover file missing: {cover}")
        if not topics:
            issues.append(f"{path.name}: missing topics")
        for topic in topics:
            if topic != topic.lower() or " " in topic:
                issues.append(f"{path.name}: topic should be lowercase kebab-case: {topic}")
        for tag in tags:
            if tag != tag.lower() or " " in tag:
                issues.append(f"{path.name}: tag should be lowercase kebab-case: {tag}")

        # Short posts are not a build blocker. They are candidates for future refresh
        # or hub curation, but concise field notes can still be valid professional content.

    return issues


def main() -> int:
    issues = audit()
    if issues:
        print("Content metadata audit: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Content metadata audit: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
