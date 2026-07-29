#!/usr/bin/env python3
"""Remove links to external official deployed sites while keeping HTML elements."""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\mainfolder.com")

# External domains to remove
EXTERNAL_DOMAINS = [
    'browsehappy.com',
    'digigro.tech',
    'vimeo.com',
    'www.opspod.in',
    'opspod.in',
    'www.turiya.co',
    'turiya.co',
]

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
total_links_removed = 0

for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content

    # Find all href attributes and check if they point to external domains
    def replace_external_href(match):
        global total_links_removed
        full_match = match.group(0)
        quote = match.group(1)
        url = match.group(2)

        # Check if URL contains any external domain
        for domain in EXTERNAL_DOMAINS:
            if domain.lower() in url.lower():
                # Remove the href attribute (including preceding whitespace)
                total_links_removed += 1
                return ''  # Remove href attribute entirely

        return full_match  # Keep if not external

    # Pattern to match href="..." or href='...'
    href_pattern = re.compile(r'\s*href=(["\'])([^"\']+)\1')

    content = href_pattern.sub(replace_external_href, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        total_files += 1
        print(f'Updated: {os.path.relpath(filepath, BASE)}')

print()
print(f'Total files updated: {total_files}')
print(f'Total external links removed: {total_links_removed}')

# Verification
print()
print('=== VERIFICATION ===')
remaining = 0
for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    for domain in EXTERNAL_DOMAINS:
        # Check if domain still appears in href
        pattern = r'href=(["\'])(' + re.escape(domain) + r'[^"\']*)\1'
        matches = re.findall(pattern, content, re.IGNORECASE)
        remaining += len(matches)

print(f'Remaining external links: {remaining}')
if remaining == 0:
    print('SUCCESS: All external site links removed!')
else:
    print('WARNING: Some external links still remain')
