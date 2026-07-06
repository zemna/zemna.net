#!/usr/bin/env python3
"""Verify built zemna.net output after professional blog upgrades."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

REQUIRED = [
    PUBLIC / "index.html",
    PUBLIC / "blog" / "index.html",
    PUBLIC / "start-here" / "index.html",
    PUBLIC / "uses" / "index.html",
    PUBLIC / "blog" / "zero-cost-observability-agent-crons" / "index.html",
]


def fail(msg: str, issues: list[str]) -> None:
    issues.append(msg)


def jsonld_blocks(html: str) -> list[dict]:
    blocks = re.findall(r'<script[^>]+type=(?:"application/ld\+json"|application/ld\+json)[^>]*>(.*?)</script>', html, re.S)
    return [json.loads(block) for block in blocks]


def graph_types(data: dict) -> set[str]:
    types: set[str] = set()
    for item in data.get("@graph", []):
        if isinstance(item, dict) and isinstance(item.get("@type"), str):
            types.add(item["@type"])
    return types


def main() -> int:
    issues: list[str] = []

    for path in REQUIRED:
        if not path.exists():
            fail(f"missing built page: {path.relative_to(ROOT)}", issues)

    if issues:
        for issue in issues:
            print(f"- {issue}")
        return 1

    home = (PUBLIC / "index.html").read_text(errors="replace")
    post = (PUBLIC / "blog" / "zero-cost-observability-agent-crons" / "index.html").read_text(errors="replace")
    blog = (PUBLIC / "blog" / "index.html").read_text(errors="replace")
    sitemap = (PUBLIC / "sitemap.xml").read_text(errors="replace")
    css = (PUBLIC / "css" / "article.min.css").read_text(errors="replace")

    for label, html, required_types in [
        ("home", home, {"WebSite", "Person", "ProfilePage"}),
        ("post", post, {"WebSite", "Person", "BreadcrumbList", "BlogPosting"}),
        ("blog", blog, {"WebSite", "Person", "BreadcrumbList", "CollectionPage"}),
    ]:
        blocks = jsonld_blocks(html)
        if not blocks:
            fail(f"{label}: missing JSON-LD", issues)
            continue
        types = set()
        for block in blocks:
            types |= graph_types(block)
        missing = required_types - types
        if missing:
            fail(f"{label}: missing JSON-LD types {sorted(missing)}", issues)

    if "grid-template-columns:minmax(0,var(--zn-article-copy-width))minmax(220px,var(--zn-article-toc-width))" not in css.replace(" ", ""):
        fail("css: article TOC/right rail grid is missing", issues)
    for banned in ["facebook.com/sharer", "api.whatsapp.com", "reddit.com/submit", "t.me/share", "mailto:?subject"]:
        if banned in post:
            fail(f"post: untrimmed share target remains: {banned}", issues)
    if "zn-related-card" not in post:
        fail("post: text-first related cards missing", issues)
    if ".webp" not in post or "<picture" not in post:
        fail("post: WebP picture output missing", issues)
    if "/posts/" in sitemap:
        fail("sitemap: legacy /posts/ URL found", issues)
    if "Start Here" not in home or "/start-here/" not in home:
        fail("home: Start Here link missing", issues)

    if issues:
        print("Built site verification: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("Built site verification: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
