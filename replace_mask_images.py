#!/usr/bin/env python3
"""
Replace all data-mask-src attributes with placehold.co URLs.
Original paths preserved in data-original-mask-src attributes.
"""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com")
PLACEHOLDER_PREFIX = "https://placehold.co"
EXCLUDE_DIRS = set()


def process_file(filepath):
    """Process a single HTML file, replacing all data-mask-src attributes."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  SKIP (read error): {filepath} — {e}")
        return 0

    original = content
    replacements = 0

    pattern = re.compile(
        r'data-mask-src\s*=\s*["\']([^"\']+)["\']',
        re.IGNORECASE
    )

    def replace_mask(m):
        nonlocal replacements
        full_match = m.group(0)
        old_src = m.group(1)

        if 'placehold.co' in old_src:
            return full_match

        new_url = f"{PLACEHOLDER_PREFIX}/300x300"

        new_attr = f'data-mask-src="{new_url}"'
        if 'data-original-mask-src' not in full_match:
            new_attr += f' data-original-mask-src="{old_src}"'

        replacements += 1
        return new_attr

    content = pattern.sub(replace_mask, content)

    if content != original:
        filepath.write_text(content, encoding='utf-8')

    return replacements


def main():
    total_files = 0
    total_masks = 0

    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for fname in files:
            if not fname.endswith('.html'):
                continue
            filepath = Path(root) / fname
            count = process_file(filepath)
            if count > 0:
                total_files += 1
                total_masks += count
                print(f"  {filepath.relative_to(BASE)} — {count} mask images replaced")

    print(f"\nDone! Replaced {total_masks} data-mask-src attributes across {total_files} files.")


if __name__ == "__main__":
    main()
