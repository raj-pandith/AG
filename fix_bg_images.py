#!/usr/bin/env python3
"""
Replace data-bg-src="assets/..." with placeholder URLs and add data-original-bg-src.

Pattern on most pages (BROKEN):
  <div ... data-bg-src="assets/img/bg/breadcumb_bg.jpg">

Pattern on home page (CORRECT):
  <div ... data-bg-src="https://placehold.co/1920x600" data-original-bg-src="assets/img/bg/category_bg_1.png">

Dimensions by folder:
  hero/   → 1920x800
  bg/     → 1920x600  (breadcrumbs, sections)
  shape/  → 400x400
"""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com")
EXCLUDE_DIRS = {"admissions-2026-27"}

# Map folders to placeholder dimensions
FOLDER_DIMS = {
    'hero': '1920x800',
    'bg': '1920x600',
    'shape': '400x400',
}


def get_placeholder_dim(original_path):
    """Determine placeholder dimensions based on the image folder."""
    for folder, dim in FOLDER_DIMS.items():
        if f'/{folder}/' in original_path:
            return dim
    return '1920x600'  # default


def fix_bg_src(content):
    """Replace data-bg-src="assets/..." with placeholder + add data-original-bg-src."""
    changed = False

    # Pattern: data-bg-src="assets/..." (without placeholder already)
    # Matches: data-bg-src="assets/img/..."
    pattern = re.compile(
        r'data-bg-src="(assets/img/[^"]+)"(?!\s+data-original-bg-src)'
    )

    def replace_match(match):
        nonlocal changed
        original_path = match.group(1)
        dim = get_placeholder_dim(original_path)
        placeholder = f'https://placehold.co/{dim}'
        changed = True
        return f'data-bg-src="{placeholder}" data-original-bg-src="{original_path}"'

    new_content = pattern.sub(replace_match, content)
    return new_content, changed


def process_file(filepath):
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  SKIP (read error): {filepath.name} — {e}")
        return False

    new_content, changed = fix_bg_src(content)

    if changed:
        filepath.write_text(new_content, encoding='utf-8')
        return True

    return False


def main():
    total = 0
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for fname in sorted(files):
            if not fname.endswith('.html'):
                continue
            filepath = Path(root) / fname
            if process_file(filepath):
                total += 1
                print(f"  {filepath.relative_to(BASE)} — bg-images replaced")

    print(f"\nDone! Replaced bg-images on {total} pages.")


if __name__ == "__main__":
    main()
