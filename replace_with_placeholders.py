#!/usr/bin/env python3
"""
Replace real image srcs with placehold.co placeholders, preserving original src in data-original-src.
"""

import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com\admissions-2026-27")
FILE = BASE / "index.html"

# Exclude these from replacement
EXCLUDE_DOMAINS = {'i.ytimg.com', 'placehold.co'}
EXCLUDE_PATHS = {'landscape-pic.png'}

with open(FILE, encoding='utf-8') as f:
    content = f.read()

# Find all img tags with width/height and real src
# Pattern: <img ... src="REAL_URL" ... width="W" height="H" ...>
# We need to replace src and add data-original-src

img_pattern = re.compile(
    r'<img\s+([^>]*?)src=["\']([^"\']+)["\']([^>]*?)/?>',
    re.DOTALL
)

def should_replace(src):
    """Check if this src should be replaced with a placeholder."""
    # Skip data URIs
    if src.startswith('data:'):
        return False
    # Skip excluded domains
    for domain in EXCLUDE_DOMAINS:
        if domain in src:
            return False
    # Skip excluded paths
    for path in EXCLUDE_PATHS:
        if path in src:
            return False
    return True


def get_dimensions(attrs):
    """Extract width and height from img tag attributes."""
    width_match = re.search(r'width=["\']?(\d+)', attrs)
    height_match = re.search(r'height=["\']?(\d+)', attrs)

    width = int(width_match.group(1)) if width_match else 300
    height = int(height_match.group(1)) if height_match else 200

    return width, height


def process_img_tag(match):
    prefix_attrs = match.group(1)  # attributes before src
    src = match.group(2)           # the src value
    suffix_attrs = match.group(3)  # attributes after src (and before >)
    full_tag = match.group(0)

    if not should_replace(src):
        return full_tag

    # Get dimensions from the full tag
    width, height = get_dimensions(full_tag)

    # Create placeholder URL
    placeholder = f"https://placehold.co/{width}x{height}"

    # Check if data-original-src already exists
    if 'data-original-src' not in full_tag:
        # Add data-original-src before the closing />
        # We need to insert it into suffix_attrs
        suffix_attrs = f' data-original-src="{src}"' + suffix_attrs

    # Replace src with placeholder
    new_tag = f'<img {prefix_attrs}src="{placeholder}"{suffix_attrs}>'

    return new_tag


# Process all img tags
new_content = img_pattern.sub(process_img_tag, content)

# Count changes
original_imgs = img_pattern.findall(content)
replaced_count = 0
for prefix, src, suffix in original_imgs:
    if should_replace(src):
        replaced_count += 1

# Write back
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Replaced {replaced_count} image srcs with placeholders")
print(f"Original srcs preserved in data-original-src attributes")
