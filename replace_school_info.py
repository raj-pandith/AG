#!/usr/bin/env python3
"""Replace all school name and contact number references with dummy text across all pages."""

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

# Define replacements (old_text, new_text, case_sensitive)
REPLACEMENTS = [
    # School name variations - text content
    ('Jain Heritage School', 'Lorem Ipsum School', True),
    ('jain heritage school', 'lorem ipsum school', True),
    ('JainHeritageSchool', 'LoremIpsumSchool', True),

    # JHS abbreviation
    ('JHS', '', True),

    # Domain in URLs - replace with example.com
    ('jainheritageschool.com', 'example.com', True),
    ('JainHeritageSchool.com', 'Example.com', True),

    # Phone numbers - replace with dummy number
    ('+918951361981', '+919876543210', True),
    ('+918951361982', '+919876543211', True),
    ('+91 8951361981', '+91 98765 43210', True),
    ('+91 8951361982', '+91 98765 43211', True),
    ('8951361981', '9876543210', True),
    ('8951361982', '9876543211', True),

    # Email addresses with school name
    ('info@jainheritageschool.com', 'info@example.com', True),
    ('admissions@jainheritageschool.com', 'admissions@example.com', True),
]

total_files = 0
total_replacements = 0
replacement_details = {}

for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content
    file_replacements = {}

    for old_text, new_text, case_sensitive in REPLACEMENTS:
        if case_sensitive:
            count = content.count(old_text)
            if count > 0:
                content = content.replace(old_text, new_text)
                file_replacements[old_text] = count
                total_replacements += count
        else:
            # Case-insensitive replacement
            pattern = re.compile(re.escape(old_text), re.IGNORECASE)
            matches = pattern.findall(content)
            if matches:
                content = pattern.sub(new_text, content)
                file_replacements[old_text] = len(matches)
                total_replacements += len(matches)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        total_files += 1
        rel_path = os.path.relpath(filepath, BASE)
        replacement_details[rel_path] = file_replacements
        print(f'Updated: {rel_path}')
        for old, count in file_replacements.items():
            print(f'  - Replaced "{old[:40]}" {count} time(s)')

print()
print(f'Total files updated: {total_files}')
print(f'Total replacements made: {total_replacements}')

# Verification
print()
print('=== VERIFICATION ===')
remaining_counts = {}
for old_text, _, _ in REPLACEMENTS:
    count = 0
    for filepath in html_files:
        with open(filepath, encoding='utf-8') as f:
            content = f.read()
        count += content.count(old_text)
    if count > 0:
        remaining_counts[old_text] = count

if remaining_counts:
    print('Remaining occurrences:')
    for text, count in sorted(remaining_counts.items(), key=lambda x: -x[1]):
        print(f'  {text}: {count}')
else:
    print('SUCCESS: All school name and contact number references removed!')
