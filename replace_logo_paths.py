#!/usr/bin/env python3
"""Replace all logo image paths with the new navbar logo path in all HTML files."""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com")

# Find all HTML files
html_files = []
for root, dirs, files in os.walk(BASE):
    skip = ['hts-cache', 'wp-content', 'wp-includes']
    if any(s in root for s in skip):
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

# New logo path - all logos should use this
NEW_LOGO_PATH = 'assets/ojixs/logo/nav-logo.png'

total_files = 0
total_replacements = 0

class Counter:
    def __init__(self):
        self.count = 0

for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content
    file_counter = Counter()

    # Find all img tags with logo references
    # Pattern: img tags containing "logo" in src, data-original-src, or class
    img_pattern = re.compile(r'<img\b[^>]*>', re.IGNORECASE)

    def replace_logo_img(match):
        file_counter.count += 1
        tag = match.group(0)

        # Check if this img tag has logo references
        has_logo = False

        # Check src attribute
        src_m = re.search(r'\ssrc=(["\'])([^"\']*logo[^"\']*)\1', tag, re.IGNORECASE)
        if src_m:
            has_logo = True

        # Check data-original-src
        if 'data-original-src' in tag and re.search(r'data-original-src=(["\'])[^"\']*logo[^"\']*\1', tag, re.IGNORECASE):
            has_logo = True

        # Check class for logo
        if re.search(r'class=(["\'])[^"\']*logo[^"\']*\1', tag, re.IGNORECASE):
            has_logo = True

        if not has_logo:
            return tag

        # Replace the src attribute with the new logo path
        # Keep the original data-original-src if it exists
        new_tag = tag

        # Find and replace src
        src_pattern = re.compile(r'(\s)src=(["\'])([^"\']+)\2', re.IGNORECASE)
        src_match = src_pattern.search(tag)
        if src_match:
            old_src = src_match.group(3)
            new_tag = new_tag.replace(src_match.group(0), src_match.group(1) + 'src=' + src_match.group(2) + NEW_LOGO_PATH + src_match.group(2), 1)
            file_counter.count += 1

        return new_tag

    content = img_pattern.sub(replace_logo_img, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        total_files += 1
        total_replacements += file_counter.count
        rel = os.path.relpath(filepath, BASE)
        print('Updated: ' + rel + ' (' + str(file_counter.count) + ' logos)')

print()
print('Total files updated: ' + str(total_files))
print('Total logo replacements: ' + str(total_replacements))

# Verification
print()
print('=== VERIFICATION ===')
remaining = 0
for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    # Find img tags with logo in src
    img_pattern = re.compile(r'<img\b[^>]*src=[^>]*logo[^>]*>', re.IGNORECASE)
    remaining += len(img_pattern.findall(content))

if remaining == 0:
    print('[SUCCESS] All logo images have been updated!')
else:
    print('[WARNING] ' + str(remaining) + ' logo images still need updating')
