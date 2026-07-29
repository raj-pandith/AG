#!/usr/bin/env python3
"""
Comprehensive image replacement for admissions-2026-27/index.html
Replaces ALL image srcs including: img src, data-lazy-src, data-thumb, etc.
"""

import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\mainfolder.com\admissions-2026-27")
FILE = BASE / "index.html"

with open(FILE, encoding='utf-8') as f:
    content = f.read()

total_replaced = 0
details = []

# ============================================================
# 1. <img> tags - replace src AND data-lazy-src
# ============================================================
img_pattern = re.compile(r'<img\b[^>]*>', re.DOTALL)

def get_placeholder(tag, default_w=300, default_h=200):
    """Generate a placeholder URL from img dimensions."""
    wm = re.search(r'width=(["\']?)(\d+)\1', tag)
    hm = re.search(r'height=(["\']?)(\d+)\1', tag)
    w = int(wm.group(2)) if wm else default_w
    h = int(hm.group(2)) if hm else default_h
    return f"https://placehold.co/{w}x{h}", w, h

def process_img(match):
    global total_replaced
    tag = match.group(0)

    # Skip if already placeholder in src
    src_m = re.search(r'\ssrc=(["\'])(.+?)\1', tag)
    if src_m and 'placehold.co' in src_m.group(2):
        # Still process data-lazy-src if present
        lazy_m = re.search(r'data-lazy-src=(["\'])(.+?)\1', tag)
        if lazy_m and not lazy_m.group(2).startswith('data:') and 'placehold.co' not in lazy_m.group(2):
            placeholder, _, _ = get_placeholder(tag)
            tag = tag.replace(f'data-lazy-src={lazy_m.group(1)}{lazy_m.group(2)}{lazy_m.group(1)}',
                             f'data-lazy-src={lazy_m.group(1)}{placeholder}{lazy_m.group(1)}')
            total_replaced += 1
        return tag

    if not src_m:
        return tag

    src = src_m.group(2)
    quote = src_m.group(1)

    # Skip data URIs (non-SVG), excluded domains
    if src.startswith('data:') and 'svg+xml' not in src:
        return tag
    if 'ytimg.com' in src or 'landscape-pic' in src:
        return tag

    placeholder, w, h = get_placeholder(tag)

    # Get original URL
    original = src
    if src.startswith('data:image/svg'):
        lazy_m = re.search(r'data-lazy-src=(["\'])(.+?)\1', tag)
        if lazy_m and not lazy_m.group(2).startswith('data:'):
            original = lazy_m.group(2)
        else:
            return tag

    # Remove old data-original-src
    tag = re.sub(r'\s*data-original-src=(["\'])(.+?)\1', '', tag)

    # Replace src
    tag = re.sub(
        r'(\ssrc=)(["\'])(' + re.escape(src) + r')\2',
        f'\\1\\2{placeholder}\\2 data-original-src=\\2{original}\\2',
        tag, count=1
    )

    # Replace data-lazy-src
    lazy_m = re.search(r'data-lazy-src=(["\'])(.+?)\1', tag)
    if lazy_m:
        lazy_src = lazy_m.group(2)
        if not lazy_src.startswith('data:') and 'placehold.co' not in lazy_src:
            tag = tag.replace(f'data-lazy-src={lazy_m.group(1)}{lazy_src}{lazy_m.group(1)}',
                             f'data-lazy-src={lazy_m.group(1)}{placeholder}{lazy_m.group(1)}')

    # Replace srcset if present
    srcset_m = re.search(r'\ssrcset=(["\'])(.+?)\1', tag)
    if srcset_m:
        entries = srcset_m.group(2).split(',')
        new_entries = []
        for entry in entries:
            entry = entry.strip()
            if ' ' in entry:
                url_part, desc = entry.rsplit(' ', 1)
                wm2 = re.search(r'(\d+)', desc)
                ew = int(wm2.group(1)) if wm2 else w
                if not url_part.startswith('data:') and 'placehold.co' not in url_part:
                    new_entries.append(f"https://placehold.co/{ew}x{h} {desc}")
                else:
                    new_entries.append(entry)
            else:
                if not entry.startswith('data:') and 'placehold.co' not in entry:
                    new_entries.append(f"https://placehold.co/{w}x{h}")
                else:
                    new_entries.append(entry)
        tag = re.sub(
            r'(\ssrcset=)(["\'])(.+?)\2',
            f'\\1\\2{", ".join(new_entries)}\\2',
            tag, count=1
        )

    total_replaced += 1
    return tag

content = img_pattern.sub(process_img, content)

# ============================================================
# 2. data-thumb attributes (slider thumbnail URLs)
# ============================================================
data_thumb_pattern = re.compile(r'(data-thumb=)(["\'])([^"\']+)\2')

def process_data_thumb(match):
    global total_replaced
    url = match.group(3)
    if 'placehold.co' in url or url.startswith('data:'):
        return match.group(0)
    placeholder = "https://placehold.co/50x100"
    total_replaced += 1
    return f'{match.group(1)}{match.group(2)}{placeholder}{match.group(2)}'

content = data_thumb_pattern.sub(process_data_thumb, content)

# ============================================================
# 3. data-bg attributes (section backgrounds)
# ============================================================
data_bg_pattern = re.compile(r'(data-bg=)(["\'])([^"\']+)\2')

def process_data_bg(match):
    global total_replaced
    url = match.group(3)
    if 'placehold.co' in url or url.startswith('data:'):
        return match.group(0)
    placeholder = "https://placehold.co/1200x800"
    total_replaced += 1
    return f'{match.group(1)}{match.group(2)}{placeholder}{match.group(2)}'

content = data_bg_pattern.sub(process_data_bg, content)

# ============================================================
# 4. style attributes with background-image: url(...)
# ============================================================
style_bg_pattern = re.compile(
    r'(background(?:-image)?[^;]*url\(\s*)(["\']?)(https?://[^"\')]+)\2(\s*\))',
    re.IGNORECASE
)

def process_style_bg(match):
    global total_replaced
    url = match.group(3)
    if 'placehold.co' in url:
        return match.group(0)
    placeholder = "https://placehold.co/1200x800"
    total_replaced += 1
    return f"{match.group(1)}{match.group(2)}{placeholder}{match.group(2)}{match.group(4)}"

content = style_bg_pattern.sub(process_style_bg, content)

# Write back
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Total images replaced: {total_replaced}")

# Verify
with open(FILE, encoding='utf-8') as f:
    content = f.read()

# Check img tags
img_tags = re.findall(r'<img\b[^>]*>', content, re.DOTALL)
real_src = 0
real_lazy = 0
placeholder_src = 0
data_uri = 0
excluded = 0

for t in img_tags:
    src_m = re.search(r'\ssrc=(["\'])(.+?)\1', t)
    lazy_m = re.search(r'data-lazy-src=(["\'])(.+?)\1', t)

    if src_m:
        src = src_m.group(2)
        if 'placehold.co' in src:
            placeholder_src += 1
        elif src.startswith('data:'):
            data_uri += 1
        elif 'ytimg' in src or 'landscape-pic' in src:
            excluded += 1
        else:
            real_src += 1

    if lazy_m:
        lazy = lazy_m.group(2)
        if not lazy.startswith('data:') and 'placehold.co' not in lazy and 'ytimg' not in lazy:
            real_lazy += 1

print(f"\nImg tags summary (total: {len(img_tags)}):")
print(f"  Placeholder src: {placeholder_src}")
print(f"  Data URI: {data_uri}")
print(f"  Excluded: {excluded}")
print(f"  Still real src: {real_src}")
print(f"  Still real data-lazy-src: {real_lazy}")

# Check data-thumb
thumbs = re.findall(r'data-thumb="([^"]+)"', content)
real_thumbs = [t for t in thumbs if 'placehold.co' not in t]
print(f"\ndata-thumb: {len(real_thumbs)} still have real URLs")

# Check data-bg
bgs = re.findall(r'data-bg="([^"]+)"', content)
real_bgs = [b for b in bgs if 'placehold.co' not in b]
print(f"data-bg: {len(real_bgs)} still have real URLs")

# Show any remaining issues
if real_src > 0 or real_lazy > 0:
    print("\n=== REMAINING REAL URLS ===")
    for t in img_tags:
        src_m = re.search(r'\ssrc=(["\'])(.+?)\1', t)
        lazy_m = re.search(r'data-lazy-src=(["\'])(.+?)\1', t)
        if src_m and 'placehold.co' not in src_m.group(2) and not src_m.group(2).startswith('data:'):
            print(f"  src: {src_m.group(2)[:100]}")
        if lazy_m and 'placehold.co' not in lazy_m.group(2) and not lazy_m.group(2).startswith('data:'):
            print(f"  lazy: {lazy_m.group(2)[:100]}")
