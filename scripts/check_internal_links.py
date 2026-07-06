#!/usr/bin/env python3
"""Check internal links in built public HTML."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

SKIP_PREFIXES = ("#", "mailto:", "tel:", "javascript:")


def target_exists(href: str) -> bool:
    parsed = urlparse(href)
    if parsed.scheme in {"http", "https"}:
        if parsed.netloc and parsed.netloc != "zemna.net":
            return True
        path = parsed.path
    else:
        path = parsed.path
    if not path or path == "/":
        return (PUBLIC / "index.html").exists()
    if path.endswith("/"):
        return (PUBLIC / path.lstrip("/") / "index.html").exists()
    candidate = PUBLIC / path.lstrip("/")
    return candidate.exists() or (candidate / "index.html").exists()


def main() -> int:
    issues: list[str] = []
    for html_path in PUBLIC.rglob("*.html"):
        text = html_path.read_text(errors="replace")
        for href in re.findall(r'href=["\']([^"\']+)["\']|href=([^\s>]+)', text):
            raw = href[0] or href[1]
            if raw.startswith(SKIP_PREFIXES) or "+" in raw or "'" in raw or '"' in raw:
                continue
            if raw.startswith("//"):
                continue
            parsed = urlparse(raw)
            if parsed.scheme in {"http", "https"} and parsed.netloc != "zemna.net":
                continue
            if not target_exists(raw):
                issues.append(f"{html_path.relative_to(PUBLIC)} -> {raw}")
    if issues:
        print("Internal link check: FAIL")
        for issue in issues[:100]:
            print(f"- {issue}")
        if len(issues) > 100:
            print(f"... {len(issues)-100} more")
        return 1
    print("Internal link check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
