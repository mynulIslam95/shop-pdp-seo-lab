"""Fail if a product page is missing core on-page SEO."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "docs"
NEED = [
    r"<title>.{10,70}</title>",
    r'<meta name="description" content=".{40,160}"',
    r'<link rel="canonical"',
    r'<meta property="og:title"',
    r'<h1>',
    r'application/ld\+json',
]


def check(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    missing = [pat for pat in NEED if not re.search(pat, html, re.I | re.S)]
    return missing


def main() -> int:
    skip = {"seo.html", "index.html"}
    pages = sorted(p for p in ROOT.glob("*.html") if p.name not in skip)
    failed = 0
    for page in pages:
        missing = check(page)
        if missing:
            failed += 1
            print(f"FAIL {page.name}: {missing}")
        else:
            print(f"OK   {page.name}")
    if not pages:
        print("No HTML in docs/. Run python3 generate_site.py first.")
        return 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
