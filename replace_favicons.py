#!/usr/bin/env python3
"""Replace all assets/img/favicons/* paths with absolute placeholder URLs."""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com")

class Counter:
    def __init__(self):
        self.files = 0
        self.replacements = 0

counter = Counter()

# Find all HTML files
html_files = []
for root, dirs, files in os.walk(BASE):
    skip = ['hts-cache', 'wp-content', 'wp-includes']
    if any(s in root for s in skip):
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content
    file_count = 0

    # Match any path starting with assets/img/favicons/
    # Extract size from filename and replace with placeholder
    favicon_pattern = re.compile(r'assets/img/favicons/[^\s"\'<>]+')

    file_count = Counter()
    global_count = Counter()

    def replace_match(match):
        file_count.replacements += 1
        global_count.replacements += 1

        path = match.group(0)
        size_match = re.search(r'(\d+)x(\d+)', path)
        if size_match:
            w, h = size_match.group(1), size_match.group(2)
            return 'https://placehold.co/' + w + 'x' + h + '.png'
        else:
            return 'https://placehold.co/16x16.png'

    content = favicon_pattern.sub(replace_match, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        counter.files += 1
        print('Updated: ' + os.path.relpath(filepath, BASE) + ' (' + str(file_count.replacements) + ' replacements)')

print()
print('Total files updated: ' + str(counter.files))
print('Total favicon references replaced: ' + str(counter.replacements))

# Verification
print()
print('=== VERIFICATION ===')
remaining = 0
for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    matches = favicon_pattern.findall(content)
    remaining += len(matches)

if remaining == 0:
    print('[CLEAN] No assets/img/favicons/* references remain!')
else:
    print('[WARNING] ' + str(remaining) + ' favicon references still remain')
