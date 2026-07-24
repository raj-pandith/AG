#!/usr/bin/env python3
"""Replace real image URLs with placeholders in admissions-2026-27, preserving original URLs."""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com\admissions-2026-27")

# Find all HTML files in admissions-2026-27
html_files = []
for root, dirs, files in os.walk(BASE):
    skip = ['hts-cache', 'wp-content', 'wp-includes']
    if any(s in root for s in skip):
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

total_files = 0
total_replaced = 0

class Counter:
    def __init__(self):
        self.count = 0

for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content
    file_counter = Counter()

    # Pattern to match img tags with real image URLs (not placeholders)
    # We need to handle both src and data-original-src attributes

    # Find all img tags
    img_pattern = re.compile(r'<img\b[^>]*>', re.DOTALL | re.IGNORECASE)

    def replace_img_src(match):
        file_counter.count += 1
        tag = match.group(0)

        # Skip if already has placehold.co in src
        if 'placehold.co' in tag and 'src=' in tag:
            return tag

        # Find src attribute
        src_m = re.search(r'\ssrc=(["\'])(.+?)\1', tag)
        if not src_m:
            return tag

        src_url = src_m.group(2)
        quote = src_m.group(1)

        # Skip data URIs, external CDNs, already processed
        if src_url.startswith('data:'):
            return tag
        if 'placehold.co' in src_url:
            return tag
        if 'fonts.googleapis.com' in src_url or 'fonts.gstatic.com' in src_url:
            return tag
        if 'googletagmanager.com' in src_url:
            return tag
        if 'ytimg.com' in src_url or 'youtube.com' in src_url:
            return tag
        if 'gravatar.com' in src_url:
            return tag

        # Check if it's an image URL
        if not re.search(r'\.(jpg|jpeg|png|webp|gif|svg|ico)', src_url, re.IGNORECASE):
            # Also check if it contains img/ or uploads/
            if 'img/' not in src_url and 'uploads/' not in src_url:
                return tag

        # Extract dimensions from tag
        w, h = 300, 200
        w_m = re.search(r'width=(["\']?)(\d+)\1', tag)
        h_m = re.search(r'height=(["\']?)(\d+)\1', tag)
        if w_m:
            w = int(w_m.group(2))
        if h_m:
            h = int(h_m.group(2))

        # Create placeholder URL
        placeholder = 'https://placehold.co/' + str(w) + 'x' + str(h)

        # Replace src with placeholder, keep original in data-original-src
        # Remove any existing data-original-src first
        tag = re.sub(r'\s*data-original-src=(["\'])(.+?)\1', '', tag)

        # Replace src attribute
        old_src = 'src=' + quote + src_url + quote
        new_src = 'src=' + quote + placeholder + quote + ' data-original-src=' + quote + src_url + quote
        tag = tag.replace(old_src, new_src, 1)

        return tag

    content = img_pattern.sub(replace_img_src, content)

    # Also handle background images in style attributes or data-bg
    # Pattern: data-bg="url" or style="background-image:url(...)"
    bg_pattern = re.compile(r'(data-bg|style)=(["\'])([^"\']*?)(url\([\"\']?)([^\"\')]+)([\"\']?\))([^"\']*?)\2', re.IGNORECASE)

    def replace_bg(match):
        file_counter.count += 1
        attr_name = match.group(1)
        quote = match.group(2)
        prefix = match.group(3)
        url_open = match.group(4)
        url = match.group(5)
        url_close = match.group(6)
        suffix = match.group(7)

        # Skip if already placeholder
        if 'placehold.co' in url:
            return match.group(0)

        # Skip data URIs and external CDNs
        if url.startswith('data:'):
            return match.group(0)
        if 'fonts.googleapis.com' in url or 'fonts.gstatic.com' in url:
            return match.group(0)

        # Check if it's an image
        if not re.search(r'\.(jpg|jpeg|png|webp|gif|svg|ico)', url, re.IGNORECASE):
            if 'img/' not in url and 'uploads/' not in url:
                return match.group(0)

        # Replace with placeholder
        placeholder = 'https://placehold.co/1200x800'
        file_replaced += 1

        return attr_name + '=' + quote + prefix + url_open + placeholder + url_close + suffix + quote

    content = bg_pattern.sub(replace_bg, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        total_files += 1
        total_replaced += file_counter.count
        rel = os.path.relpath(filepath, BASE)
        print('Updated: ' + rel + ' (' + str(file_counter.count) + ' images)')

print()
print('Total files updated: ' + str(total_files))
print('Total images replaced: ' + str(total_replaced))

# Verification
print()
print('=== VERIFICATION ===')
remaining = 0
for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    # Check for real loading images (not placeholders, not data URIs)
    src_pattern = re.compile(r'src=\"([^\"]+)\"')
    for match in src_pattern.finditer(content):
        src = match.group(1)
        if 'placehold.co' not in src and not src.startswith('data:'):
            if re.search(r'\.(jpg|jpeg|png|webp|gif|svg|ico)', src, re.IGNORECASE):
                remaining += 1

if remaining == 0:
    print('[CLEAN] No real loading images remain!')
else:
    print('[WARNING] ' + str(remaining) + ' real images still load')
