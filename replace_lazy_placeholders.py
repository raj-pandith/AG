#!/usr/bin/env python3
"""
Replace data: SVG placeholder srcs with placehold.co placeholders, preserving original in data-original-src.
For lazy-loaded images that have data-lazy-src, use that as the original URL.
"""

import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\mainfolder.com\admissions-2026-27")
FILE = BASE / "index.html"

with open(FILE, encoding='utf-8') as f:
    content = f.read()

# Find all img tags with src="data:image/svg+xml..."
pattern = re.compile(r'<img\s+([^>]*?)src="data:image/svg\+xml[^"]*"([^>]*?)/?>', re.DOTALL)

def process_img_tag(match):
    prefix_attrs = match.group(1)
    suffix_attrs = match.group(2)
    full_tag = match.group(0)

    # Get dimensions
    width_match = re.search(r'width=["\']?(\d+)', full_tag)
    height_match = re.search(r'height=["\']?(\d+)', full_tag)

    width = int(width_match.group(1)) if width_match else 300
    height = int(height_match.group(1)) if height_match else 200

    # Get original src from data-lazy-src if present, otherwise from data-original-src
    lazy_src_match = re.search(r'data-lazy-src="([^"]+)"', full_tag)
    orig_src_match = re.search(r'data-original-src="([^"]+)"', full_tag)

    if orig_src_match:
        original_src = orig_src_match.group(1)
    elif lazy_src_match:
        original_src = lazy_src_match.group(1)
        # Remove data-lazy-src since we won't need lazy loading with placeholder
        suffix_attrs = suffix_attrs.replace(f' data-lazy-src="{lazy_src_match.group(1)}"', '')
    else:
        # No original found, use the data URI as original
        original_src = match.group(0).split('src="')[1].split('"')[0]

    # Create placeholder URL
    placeholder = f"https://placehold.co/{width}x{height}"

    # Remove any existing data-original-src
    suffix_attrs = re.sub(r'\s*data-original-src="[^"]*"', '', suffix_attrs)

    # Add new data-original-src
    suffix_attrs = f' data-original-src="{original_src}"' + suffix_attrs

    new_tag = f'<img {prefix_attrs}src="{placeholder}"{suffix_attrs}>'
    return new_tag


new_content = pattern.sub(process_img_tag, content)
count = len(pattern.findall(content))

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Replaced {count} lazy-loaded data: SVG placeholders with placehold.co URLs")
print(f"Original URLs preserved in data-original-src attributes (from data-lazy-src)")
