#!/usr/bin/env python3
"""Generate lightweight WebP siblings for static site images.

The originals stay untouched. Hugo templates and render hooks can serve the WebP
version through <picture> while keeping the original as fallback.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "static"
TARGET_DIRS = [STATIC / "covers", STATIC / "img", STATIC / "images"]
EXTS = {".png", ".jpg", ".jpeg"}


def command_exists(name: str) -> bool:
    return subprocess.run(["bash", "-lc", f"command -v {name} >/dev/null 2>&1"], cwd=ROOT).returncode == 0


def image_size(path: Path) -> tuple[int, int] | None:
    proc = subprocess.run(
        ["identify", "-format", "%w %h", str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        return None
    w, h = proc.stdout.strip().split()
    return int(w), int(h)


def iter_images() -> list[Path]:
    images: list[Path] = []
    for directory in TARGET_DIRS:
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if path.suffix.lower() in EXTS and not path.name.endswith(".webp"):
                images.append(path)
    return sorted(images)


def convert_image(src: Path, force: bool = False) -> bool:
    dst = src.with_suffix(".webp")
    if dst.exists() and not force and dst.stat().st_mtime >= src.stat().st_mtime:
        return False

    size = image_size(src)
    resize: list[str] = []
    if size and size[0] > 1600:
        resize = ["-resize", "1600x1600>"]

    cmd = ["convert", str(src), "-auto-orient", *resize, "-strip", "-quality", "82", str(dst)]
    subprocess.run(cmd, cwd=ROOT, check=True)
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Report missing/stale WebP siblings without writing files")
    parser.add_argument("--force", action="store_true", help="Regenerate all WebP siblings")
    args = parser.parse_args()

    for required in ["identify", "convert"]:
        if not command_exists(required):
            print(f"Missing required command: {required}", file=sys.stderr)
            return 2

    images = iter_images()
    missing = []
    generated = []
    for src in images:
        dst = src.with_suffix(".webp")
        stale = (not dst.exists()) or dst.stat().st_mtime < src.stat().st_mtime
        if args.check:
            if stale:
                missing.append(str(src.relative_to(ROOT)))
            continue
        if convert_image(src, force=args.force):
            generated.append(str(dst.relative_to(ROOT)))

    if args.check:
        if missing:
            print("Image optimization check: FAIL")
            for item in missing:
                print(f"- missing or stale WebP: {item}")
            return 1
        print(f"Image optimization check: PASS ({len(images)} source images)")
        return 0

    print(f"Generated or refreshed {len(generated)} WebP files from {len(images)} source images")
    for item in generated[:50]:
        print(f"- {item}")
    if len(generated) > 50:
        print(f"... {len(generated) - 50} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
