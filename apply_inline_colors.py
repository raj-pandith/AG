#!/usr/bin/env python3
"""Replace colors in inline styles across all HTML files."""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\mainfolder.com")

# Find all HTML files
html_files = []
for root, dirs, files in os.walk(BASE):
    skip = ['hts-cache', 'wp-content', 'wp-includes']
    if any(s in root for s in skip):
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

# Color replacements - case insensitive
COLOR_MAP = {
    # Primary dark
    '1a2653': '7c381a',
    '001c54': '7c381a',
    '001C49': '7c381a',
    '0b1422': '7c381a',
    '113D48': '7c381a',
    # Golden accents
    'F8BC22': 'f3bb1d',
    'FFB539': 'f3bb1d',
    'FFA944': 'f3bb1d',
    'ffa500': 'f3bb1d',
    # Backgrounds
    'F2F5FA': 'fffef4',
    'E9F6F9': 'fdf8d8',
    'F3F4F6': 'fdf8d8',
    # Grays to butter cream
    'E1E4E5': 'fdf8d8',
    'E1E4E6': 'fdf8d8',
    'B1B8C3': 'f9e277',
}

total_files = 0
total_replacements = 0

for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content
    file_replacements = 0

    # Replace each color (case insensitive)
    for old, new in COLOR_MAP.items():
        # Use regex with case-insensitive matching
        pattern = re.compile(re.escape('#' + old), re.IGNORECASE)
        matches = pattern.findall(content)
        if matches:
            content = pattern.sub('#' + new, content)
            file_replacements += len(matches)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        total_files += 1
        total_replacements += file_replacements
        rel = os.path.relpath(filepath, BASE)
        print('Updated: ' + rel + ' (' + str(file_replacements) + ' replacements)')

print()
print('Total files updated: ' + str(total_files))
print('Total color replacements: ' + str(total_replacements))

# Verification
print()
print('=== VERIFICATION ===')
remaining = 0
for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    for old in COLOR_MAP.keys():
        pattern = re.compile(re.escape('#' + old), re.IGNORECASE)
        remaining += len(pattern.findall(content))

if remaining == 0:
    print('[SUCCESS] All old colors replaced!')
else:
    print('[WARNING] ' + str(remaining) + ' old color references still remain')
