#!/usr/bin/env python3
"""
Replace all <img> src attributes across HTML files with placehold.co URLs.
Original src is preserved in a data-original-src comment attribute.

Dimension detection order:
  1. Explicit width="" height="" HTML attributes
  2. Inline style="width: Xpx; height: Ypx;"
  3. Filename pattern: _WxH or _WXH (e.g., blog_856X450.jpg)
  4. Path-based defaults (logos, icons, blog, gallery, etc.)
  5. Fallback: 600x400
"""

import os
import re
import sys
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\mainfolder.com")
PLACEHOLDER_PREFIX = "https://placehold.co"

# Exclude the WordPress admissions directory
EXCLUDE_DIRS = {"cdn.jsdelivr.net", "cdnjs.cloudflare.com",
                "translate.google.com", "www.googletagmanager.com"}


def parse_style_dims(style_str):
    """Extract width and height from inline style attribute."""
    w, h = None, None
    if not style_str:
        return w, h
    m = re.search(r'width\s*:\s*(\d+)', style_str)
    if m:
        w = int(m.group(1))
    m = re.search(r'height\s*:\s*(\d+)', style_str)
    if m:
        h = int(m.group(1))
    return w, h


def parse_filename_dims(src):
    """Extract dimensions from filename patterns like _856X450 or _416x350."""
    basename = src.split('/')[-1].split('?')[0]
    m = re.search(r'[_\-](\d{2,4})[xX](\d{2,4})', basename)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None


def get_default_dims(src):
    """Assign default dimensions based on the image path/category."""
    src_lower = src.lower()
    basename = src_lower.split('/')[-1].split('?')[0]

    # Logos
    if 'logo' in basename or 'logo' in src_lower.split('/')[-2] if len(src_lower.split('/')) > 1 else '':
        if 'logo3' in basename or 'logo-icon3' in basename:
            return 200, 150  # Small logo icon
        return 200, 80  # Full logo

    # Icons
    if '/icon/' in src_lower:
        if 'phone' in basename or 'envelope' in basename or 'location' in basename:
            return 48, 48
        if 'search' in basename or 'plane' in basename or 'map' in basename:
            return 24, 24
        return 24, 24

    # Blog images
    if '/blog/' in src_lower:
        if '856' in basename or '856X450' in basename.upper():
            return 856, 450
        if '416' in basename or '416X350' in basename.upper():
            return 416, 350
        if '424' in basename or '424X351' in basename.upper():
            return 424, 351
        return 600, 400

    # Category images
    if '/category/' in src_lower:
        return 600, 400

    # Normal/about images
    if '/normal/' in src_lower:
        return 800, 600

    # Team images
    if '/team/' in src_lower:
        return 400, 500

    # Gallery
    if '/gallery/' in src_lower:
        return 600, 400

    # Shape elements
    if '/shape/' in src_lower:
        return 600, 400

    # General fallback
    return 600, 400


def get_img_dimensions(img_tag):
    """Determine (width, height) for an <img> tag using all available info."""
    # 1. Check explicit width/height attributes
    w_m = re.search(r'\bwidth\s*=\s*["\']?(\d+)', img_tag, re.IGNORECASE)
    h_m = re.search(r'\bheight\s*=\s*["\']?(\d+)', img_tag, re.IGNORECASE)
    w = int(w_m.group(1)) if w_m else None
    h = int(h_m.group(1)) if h_m else None

    # 2. Check inline style
    style_m = re.search(r'style\s*=\s*["\']([^"\']+)["\']', img_tag, re.IGNORECASE)
    if style_m:
        sw, sh = parse_style_dims(style_m.group(1))
        if w is None:
            w = sw
        if h is None:
            h = sh

    # 3. Check filename
    src_m = re.search(r'src\s*=\s*["\']([^"\']+)["\']', img_tag, re.IGNORECASE)
    src = src_m.group(1) if src_m else ""
    if src and (w is None or h is None):
        fw, fh = parse_filename_dims(src)
        if w is None:
            w = fw
        if h is None:
            h = fh

    # 4. Fallback defaults based on path
    if w is None or h is None:
        dw, dh = get_default_dims(src)
        if w is None:
            w = dw
        if h is None:
            h = dh

    return w, h, src


def process_file(filepath):
    """Process a single HTML file, replacing all img src attributes."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  SKIP (read error): {filepath} — {e}")
        return 0

    original = content
    replacements = 0

    # Find all <img> tags (handling multiline)
    img_pattern = re.compile(r'(<img\b[^>]*>)', re.IGNORECASE | re.DOTALL)

    def replace_img(m):
        nonlocal replacements
        tag = m.group(1)

        # Skip if already processed
        if 'data-original-src' in tag and 'placehold.co' in tag:
            return tag

        w, h, old_src = get_img_dimensions(tag)

        if not old_src:
            return tag

        # Skip if already a placehold.co URL
        if 'placehold.co' in old_src:
            return tag

        # Build new placeholder URL
        new_url = f"{PLACEHOLDER_PREFIX}/{w}x{h}"

        # Start with replacing src
        if 'src=' in tag:
            # Handle double-quoted src
            if f'src="{old_src}"' in tag:
                new_tag = tag.replace(f'src="{old_src}"', f'src="{new_url}"', 1)
            else:
                new_tag = re.sub(r"src='([^']*)'", f"src='{new_url}'", tag, count=1)
            tag = new_tag

        # Replace data-src (lazy loading)
        data_src_m = re.search(r'data-src\s*=\s*["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if data_src_m and 'placehold.co' not in data_src_m.group(1):
            old_data_src = data_src_m.group(1)
            dw, dh, _ = get_img_dimensions(tag)
            data_src_url = f"{PLACEHOLDER_PREFIX}/{dw}x{dh}"
            tag = re.sub(
                r'data-src\s*=\s*["\'][^"\']*["\']',
                f'data-src="{data_src_url}" data-original-data-src="{old_data_src}"',
                tag,
                count=1
            )

        # Replace data-lazy-src
        lazy_src_m = re.search(r'data-lazy-src\s*=\s*["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if lazy_src_m and 'placehold.co' not in lazy_src_m.group(1):
            old_lazy = lazy_src_m.group(1)
            dw, dh, _ = get_img_dimensions(tag)
            lazy_url = f"{PLACEHOLDER_PREFIX}/{dw}x{dh}"
            tag = re.sub(
                r'data-lazy-src\s*=\s*["\'][^"\']*["\']',
                f'data-lazy-src="{lazy_url}" data-original-lazy-src="{old_lazy}"',
                tag,
                count=1
            )

        # Replace srcset with a single placehold.co URL
        srcset_m = re.search(r'srcset\s*=\s*["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if srcset_m and 'placehold.co' not in srcset_m.group(1):
            old_srcset = srcset_m.group(1)
            dw, dh, _ = get_img_dimensions(tag)
            srcset_url = f"{PLACEHOLDER_PREFIX}/{dw}x{dh}"
            tag = re.sub(
                r'srcset\s*=\s*["\'][^"\']*["\']',
                f'srcset="{srcset_url}" data-original-srcset="{old_srcset}"',
                tag,
                count=1
            )

        # Add data-original-src if not already present
        if 'data-original-src' not in tag and old_src:
            tag = re.sub(
                r'(src\s*=\s*["\'][^"\']+["\'])',
                f'\\1 data-original-src="{old_src}"',
                tag,
                count=1
            )

        replacements += 1
        return tag

    content = img_pattern.sub(replace_img, content)

    if content != original:
        filepath.write_text(content, encoding='utf-8')

    return replacements


def main():
    total_files = 0
    total_imgs = 0

    for root, dirs, files in os.walk(BASE):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for fname in files:
            if not fname.endswith('.html'):
                continue
            filepath = Path(root) / fname
            count = process_file(filepath)
            if count > 0:
                total_files += 1
                total_imgs += count
                print(f"  {filepath.relative_to(BASE)} — {count} images replaced")

    print(f"\nDone! Replaced {total_imgs} <img> tags across {total_files} files.")


if __name__ == "__main__":
    main()
