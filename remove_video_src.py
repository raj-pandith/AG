#!/usr/bin/env python3
"""Remove src from video and source tags across all pages while keeping the HTML elements."""

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

total_files = 0
total_src_removed = 0

for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove src attribute from <source> tags within video elements
    # Pattern: <source src="..." type="..."> -> <source type="...">
    source_pattern = re.compile(r'<source\s+src=(["\'])[^"\']+\1([^>]*>)', re.IGNORECASE)

    def remove_source_src(match):
        global total_src_removed
        total_src_removed += 1
        # Keep everything except the src attribute
        return '<source ' + match.group(2).lstrip()

    content = source_pattern.sub(remove_source_src, content)

    # Remove src attribute from <video> tags (if any have direct src)
    video_pattern = re.compile(r'<video\s+src=(["\'])[^"\']+\1([^>]*>)', re.IGNORECASE)

    def remove_video_src(match):
        global total_src_removed
        total_src_removed += 1
        # Keep everything except the src attribute
        return '<video ' + match.group(2).lstrip()

    content = video_pattern.sub(remove_video_src, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        total_files += 1
        print('Updated: ' + os.path.relpath(filepath, BASE))

print()
print('Total files updated: ' + str(total_files))
print('Total src attributes removed: ' + str(total_src_removed))

# Verification
print()
print('=== VERIFICATION ===')
remaining_src = 0
for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    # Check for source tags with src
    source_with_src = re.findall(r'<source\s+src=', content, re.IGNORECASE)
    video_with_src = re.findall(r'<video\s+src=', content, re.IGNORECASE)
    remaining_src += len(source_with_src) + len(video_with_src)

if remaining_src == 0:
    print('[CLEAN] No src attributes remain in video/source tags!')
else:
    print('[WARNING] ' + str(remaining_src) + ' src attributes still remain')
