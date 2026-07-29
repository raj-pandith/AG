#!/usr/bin/env python3
"""
Replace all data-bg-src attributes with placehold.co URLs.
Original paths preserved in data-original-bg-src attributes.

Used by JS (main.js) to apply CSS background-image.
"""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\mainfolder.com")
PLACEHOLDER_PREFIX = "https://placehold.co"
EXCLUDE_DIRS = set()


def parse_filename_dims(src):
    """Extract dimensions from filename like _856X450 or _416x350."""
    basename = src.split('/')[-1].split('?')[0]
    m = re.search(r'[_\-](\d{2,4})[xX×](\d{2,4})', basename)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None


def guess_dims_from_context(attr_value, tag_snippet=""):
    """Estimate dimensions from the image path, filename, and surrounding HTML."""
    src_lower = attr_value.lower()
    basename = src_lower.split('/')[-1].split('?')[0]

    # 1. Check filename for embedded dimensions
    fw, fh = parse_filename_dims(src_lower)
    if fw and fh:
        return fw, fh

    # 2. Context-based defaults
    # Hero slider backgrounds (full-width, tall)
    if '/hero/' in src_lower or 'hero' in basename:
        return 1920, 800

    # Breadcrumb section backgrounds (full-width, medium height)
    if 'breadcumb' in src_lower or 'breadcum' in src_lower or 'breadcrumb' in src_lower:
        return 1920, 400

    # Blog detail backgrounds
    if 'blog_details' in src_lower or 'blog' in src_lower:
        return 1200, 400

    # Widget sidebar banners
    if 'widget_banner' in src_lower:
        return 300, 400

    # Video wrapper backgrounds
    if 'video_bg' in src_lower:
        return 1920, 600

    # Category area
    if 'category_bg' in src_lower:
        return 1920, 600

    # General section backgrounds
    if src_lower.startswith('assets/img/bg/'):
        # Try to infer from class context
        if 'service_bg' in src_lower:
            return 1920, 600
        if 'process' in src_lower:
            return 1920, 600
        if 'project' in src_lower:
            return 1920, 600
        return 1920, 600

    # Shape/decorative elements
    if '/shape/' in src_lower:
        return 300, 300

    # General fallback
    return 1920, 600


def process_file(filepath):
    """Process a single HTML file, replacing all data-bg-src attributes."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  SKIP (read error): {filepath} — {e}")
        return 0

    original = content
    replacements = 0

    # Match data-bg-src="..." attributes
    pattern = re.compile(
        r'data-bg-src\s*=\s*["\']([^"\']+)["\']',
        re.IGNORECASE
    )

    def replace_bg(m):
        nonlocal replacements
        full_match = m.group(0)
        old_src = m.group(1)

        if 'placehold.co' in old_src:
            return full_match

        w, h = guess_dims_from_context(old_src)
        new_url = f"{PLACEHOLDER_PREFIX}/{w}x{h}"

        new_attr = f'data-bg-src="{new_url}"'
        if 'data-original-bg-src' not in full_match:
            new_attr += f' data-original-bg-src="{old_src}"'

        replacements += 1
        return new_attr

    content = pattern.sub(replace_bg, content)

    if content != original:
        filepath.write_text(content, encoding='utf-8')

    return replacements


def main():
    total_files = 0
    total_bgs = 0

    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for fname in files:
            if not fname.endswith('.html'):
                continue
            filepath = Path(root) / fname
            count = process_file(filepath)
            if count > 0:
                total_files += 1
                total_bgs += count
                print(f"  {filepath.relative_to(BASE)} — {count} bg images replaced")

    print(f"\nDone! Replaced {total_bgs} data-bg-src attributes across {total_files} files.")


if __name__ == "__main__":
    main()
