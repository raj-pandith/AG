#!/usr/bin/env python3
"""Replace ALL occurrences of real image URLs with placeholders in admissions-2026-27."""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com\admissions-2026-27")

# Find all HTML files
html_files = []
for root, dirs, files in os.walk(BASE):
    skip = ['hts-cache', 'wp-content', 'wp-includes']
    if any(s in root for s in skip):
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

# Known real image URLs to replace
REAL_IMAGES = {
    # Application folder images
    'wp-content/uploads/2024/08/Campus-1024x576.jpg': 'https://placehold.co/1024x576',
    'wp-content/uploads/2024/08/img01.jpg': 'https://placehold.co/1024x768',
    'wp-content/uploads/2024/08/img03-1.jpg': 'https://placehold.co/1024x768',
    'wp-content/uploads/2024/08/img02-1-1.jpg': 'https://placehold.co/1024x768',
    'wp-content/uploads/2024/08/Dr.-Chenraj-Roychand-1-1024x683.jpg': 'https://placehold.co/1024x683',
    'wp-content/uploads/2024/08/About-Jain-Heritage-School-1024x683.jpg': 'https://placehold.co/1024x683',
    # Admissions-closing folder images
    '../wp-content/uploads/2024/08/Campus-1024x576.jpg': 'https://placehold.co/1024x576',
    '../wp-content/uploads/2024/08/img01.jpg': 'https://placehold.co/1024x768',
    '../wp-content/uploads/2024/08/img03-1.jpg': 'https://placehold.co/1024x768',
    '../wp-content/uploads/2024/08/img02-1-1.jpg': 'https://placehold.co/1024x768',
    '../wp-content/uploads/2024/08/Dr.-Chenraj-Roychand-1-1024x683.jpg': 'https://placehold.co/1024x683',
    '../wp-content/uploads/2024/08/About-Jain-Heritage-School-1024x683.jpg': 'https://placehold.co/1024x683',
    # Main index images
    'https://example.com/admissions-2026-27/wp-content/uploads/2021/03/logo-1.png': 'https://placehold.co/200x80',
    'http://example.com/admissions-2026-27/wp-content/uploads/2022/11/banner-img-4.jpg': 'https://placehold.co/1920x1080',
    'http://example.com/admissions-2026-27/wp-content/uploads/2022/10/001.jpg': 'https://placehold.co/800x600',
    'http://example.com/admissions-2026-27/wp-content/uploads/2022/10/003.jpg': 'https://placehold.co/800x600',
    'http://example.com/admissions-2026-27/wp-content/uploads/2022/10/002.jpg': 'https://placehold.co/800x600',
    'https://example.com/admissions-2026-27/wp-content/uploads/2022/11/why-video-thumb-v4.png': 'https://placehold.co/800x600',
    'http://example.com/admissions-2026-27/wp-content/uploads/2022/11/jhs-1-scaled.jpg': 'https://placehold.co/800x600',
    'http://example.com/admissions-2026-27/wp-content/uploads/2022/11/jhs-2.jpg': 'https://placehold.co/800x600',
    'http://example.com/admissions-2026-27/wp-content/uploads/2022/11/jhs-3.jpg': 'https://placehold.co/800x600',
    'http://example.com/admissions-2026-27/wp-content/uploads/2022/11/IMG20220811085633-1-scaled.jpg': 'https://placehold.co/800x600',
    'http://example.com/admissions-2026-27/wp-content/uploads/2022/11/jhs-5-scaled.jpg': 'https://placehold.co/800x600',
    'http://example.com/admissions-2026-27/wp-content/uploads/2021/03/photo-02.jpg': 'https://placehold.co/800x600',
    'http://example.com/admissions-2026-27/wp-content/uploads/2021/03/photo-02-4.jpg': 'https://placehold.co/800x600',
    'http://example.com/admissions-2026-27/wp-content/uploads/2021/03/photo-02-1.jpg': 'https://placehold.co/800x600',
    'http://example.com/admissions-2026-27/wp-content/uploads/2021/03/photo-02-3.jpg': 'https://placehold.co/800x600',
    'http://example.com/admissions-2026-27/wp-content/uploads/2021/03/photo-02-2.jpg': 'https://placehold.co/800x600',
    'https://example.com/admissions-2026-27/wp-content/uploads/2022/11/WhatsApp-Image-2022-10-19-at-11.06.07-AM.jpg': 'https://placehold.co/800x600',
    'https://example.com/admissions-2026-27/wp-content/uploads/2022/11/fd.jpg': 'https://placehold.co/800x600',
    'https://example.com/admissions-2026-27/wp-content/uploads/2022/11/311800351_478360324330223_2873886692781282713_n.jpg': 'https://placehold.co/800x600',
}

total_files = 0
total_replacements = 0

for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content
    file_replacements = 0

    # Replace all known real image URLs with placeholders
    for real_url, placeholder_url in REAL_IMAGES.items():
        if real_url in content:
            count = content.count(real_url)
            content = content.replace(real_url, placeholder_url)
            file_replacements += count

    # Also handle admissions-closing specific images
    if 'admissions-closing' in filepath:
        closing_images = {
            'https://example.com/admissions-2026-27/application/wp-content/uploads/2024/08/Art-Painting.jpg': 'https://placehold.co/800x600',
            'https://example.com/admissions-2026-27/application/wp-content/uploads/2024/08/Clay-Modeling.jpg': 'https://placehold.co/800x600',
            'https://example.com/admissions-2026-27/application/wp-content/uploads/2024/08/Dance.jpg': 'https://placehold.co/800x600',
            'https://example.com/admissions-2026-27/application/wp-content/uploads/2024/08/Music.jpg': 'https://placehold.co/800x600',
            'https://example.com/admissions-2026-27/application/wp-content/uploads/2024/08/Sports.jpg': 'https://placehold.co/800x600',
        }
        for real_url, placeholder_url in closing_images.items():
            if real_url in content:
                count = content.count(real_url)
                content = content.replace(real_url, placeholder_url)
                file_replacements += count

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        total_files += 1
        total_replacements += file_replacements
        rel = os.path.relpath(filepath, BASE)
        print('Updated: ' + rel + ' (' + str(file_replacements) + ' replacements)')

print()
print('Total files updated: ' + str(total_files))
print('Total image references replaced: ' + str(total_replacements))

# Verification
print()
print('=== VERIFICATION ===')
remaining = 0
for filepath in html_files:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    for real_url in REAL_IMAGES.keys():
        if real_url in content:
            remaining += content.count(real_url)

if remaining == 0:
    print('[CLEAN] No real image URLs remain!')
else:
    print('[WARNING] ' + str(remaining) + ' real image URLs still remain')
