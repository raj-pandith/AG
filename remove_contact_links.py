#!/usr/bin/env python3
"""Remove contact/social links from all HTML files while keeping logos/icons."""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\mainfolder.com")

# Patterns to identify contact/social links to remove
LINK_PATTERNS = [
    r'href="tel:[^"]*"',
    r'href="mailto:[^"]*"',
    r'href="[^"]*wa\.me[^"]*"',
    r'href="[^"]*instagram[^"]*"',
    r'href="[^"]*facebook[^"]*"',
    r'href="[^"]*twitter[^"]*"',
    r'href="[^"]*linkedin[^"]*"',
    r'href="[^"]*youtube\.com[^"]*"',
    r'href="[^"]*youtu\.be[^"]*"',
]

# Combined pattern to match any of the above within an <a> tag
COMBINED = '|'.join(LINK_PATTERNS)

# Find all HTML files (excluding cache and wp content)
html_files = []
for root, dirs, files in os.walk(BASE):
    # Skip directories
    skip = ['hts-cache', 'wp-content', 'wp-includes']
    if any(s in root for s in skip):
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

total_files = 0
total_links_removed = 0

for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content

    # Find all <a> tags that contain any of our target patterns
    # We need to match the href attribute specifically
    def remove_href(match):
        global total_links_removed
        tag = match.group(0)
        # Remove the href attribute and its value
        # Match href="..." or href='...'
        new_tag = re.sub(r'\s*href=(["\'])[^\1]*\1', '', tag, flags=re.DOTALL)
        total_links_removed += 1
        return new_tag

    # Pattern to match <a> tags containing any of our target URLs
    # This is a multi-line pattern that captures the entire <a>...</a> tag
    a_tag_pattern = re.compile(
        r'<a\b[^>]*?(?:' + COMBINED + r')[^>]*>.*?</a>',
        re.DOTALL | re.IGNORECASE
    )

    content = a_tag_pattern.sub(remove_href, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        total_files += 1
        print(f'Updated: {os.path.relpath(filepath, BASE)}')

print()
print(f'Total files updated: {total_files}')
print(f'Total links removed: {total_links_removed}')

# Verification
print()
print('=== VERIFICATION ===')
remaining = 0
for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    for pattern in LINK_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            remaining += len(matches)

print(f'Remaining contact/social links: {remaining}')
if remaining == 0:
    print('SUCCESS: All contact/social links removed!')
