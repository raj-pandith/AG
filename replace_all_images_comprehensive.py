#!/usr/bin/env python3
"""
COMPREHENSIVE image replacement for admissions-2026-27/index.html
Replaces EVERY image reference with placeholder, preserves original in data-original-src.
"""

import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\mainfolder.com\admissions-2026-27")
FILE = BASE / "index.html"

with open(FILE, encoding='utf-8') as f:
    content = f.read()

total_replaced = 0
details = []

IMAGE_EXTS = r'\.(jpg|jpeg|png|gif|webp|svg|bmp|ico|tiff?)(\?|#|$)'
EXCLUDE_PATTERNS = ['ytimg.com', 'landscape-pic', 'placehold.co']

def should_process(url):
    if not url or url.startswith('data:'):
        return False
    if any(excl in url for excl in EXCLUDE_PATTERNS):
        return False
    if 'jainheritageschool' not in url and not re.search(IMAGE_EXTS, url, re.IGNORECASE):
        return False
    return True

def get_placeholder_dimensions(tag_or_attrs, default_w=300, default_h=200):
    w, h = default_w, default_h
    wm = re.search(r'width=(["\']?)(\d+)\1', tag_or_attrs)
    hm = re.search(r'height=(["\']?)(\d+)\1', tag_or_attrs)
    if wm: w = int(wm.group(2))
    if hm: h = int(hm.group(2))
    return w, h

def make_placeholder(w, h):
    return "https://placehold.co/" + str(w) + "x" + str(h)

# ============================================================
# 1. <img> tags - comprehensive processing
# ============================================================
img_pattern = re.compile(r'<img\b[^>]*>', re.DOTALL)

def process_img(match):
    global total_replaced
    tag = match.group(0)

    src_m = re.search(r'\ssrc=(["\'])(.+?)\1', tag)
    if not src_m:
        return tag

    src = src_m.group(2)
    quote = src_m.group(1)

    if 'placehold.co' in src:
        return tag
    if not should_process(src):
        return tag

    w, h = get_placeholder_dimensions(tag)

    original = src
    if src.startswith('data:image/svg'):
        lazy_m = re.search(r'data-lazy-src=(["\'])(.+?)\1', tag)
        if lazy_m and should_process(lazy_m.group(2)):
            original = lazy_m.group(2)
        else:
            return tag

    placeholder = make_placeholder(w, h)

    # Remove old data-original-src
    tag = re.sub(r'\s*data-original-src=(["\'])(.+?)\1', '', tag)

    # Replace src using string replacement (not re.sub to avoid backref issues)
    old_src = 'src=' + quote + src + quote
    new_src = 'src=' + quote + placeholder + quote + ' data-original-src=' + quote + original + quote
    tag = tag.replace(old_src, new_src, 1)

    # data-lazy-src
    lazy_m = re.search(r'data-lazy-src=(["\'])(.+?)\1', tag)
    if lazy_m and should_process(lazy_m.group(2)):
        old_lazy = 'data-lazy-src=' + lazy_m.group(1) + lazy_m.group(2) + lazy_m.group(1)
        tag = tag.replace(old_lazy, 'data-lazy-src=' + lazy_m.group(1) + placeholder + lazy_m.group(1))

    # data-src
    data_src_m = re.search(r'data-src=(["\'])(.+?)\1', tag)
    if data_src_m and should_process(data_src_m.group(2)):
        old_ds = 'data-src=' + data_src_m.group(1) + data_src_m.group(2) + data_src_m.group(1)
        tag = tag.replace(old_ds, 'data-src=' + data_src_m.group(1) + placeholder + data_src_m.group(1))

    # data-retina
    retina_m = re.search(r'data-retina=(["\'])(.+?)\1', tag)
    if retina_m and should_process(retina_m.group(2)):
        old_ret = 'data-retina=' + retina_m.group(1) + retina_m.group(2) + retina_m.group(1)
        tag = tag.replace(old_ret, 'data-retina=' + retina_m.group(1) + placeholder + retina_m.group(1))

    # srcset
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
                if should_process(url_part):
                    new_entries.append(make_placeholder(ew, h) + " " + desc)
                else:
                    new_entries.append(entry)
            else:
                if should_process(entry):
                    new_entries.append(make_placeholder(w, h))
                else:
                    new_entries.append(entry)
        new_srcset = ', '.join(new_entries)
        old_srcset = 'srcset=' + srcset_m.group(1) + srcset_m.group(2) + srcset_m.group(1)
        new_srcset_attr = 'srcset=' + srcset_m.group(1) + new_srcset + srcset_m.group(1)
        tag = tag.replace(old_srcset, new_srcset_attr)

    total_replaced += 1
    details.append("img: " + original[:50] + " -> " + placeholder)
    return tag

content = img_pattern.sub(process_img, content)

# ============================================================
# 2. <source> tags with srcset
# ============================================================
source_pattern = re.compile(r'<source\b[^>]*>', re.DOTALL)

def process_source(match):
    global total_replaced
    tag = match.group(0)

    srcset_m = re.search(r'srcset=(["\'])(.+?)\1', tag)
    if not srcset_m:
        return tag

    srcset = srcset_m.group(2)
    entries = srcset.split(',')
    needs_replace = False
    new_entries = []
    for entry in entries:
        entry = entry.strip()
        if ' ' in entry:
            url_part, desc = entry.rsplit(' ', 1)
        else:
            url_part = entry
            desc = ''
        if should_process(url_part):
            needs_replace = True
            wm2 = re.search(r'(\d+)', desc)
            w = int(wm2.group(1)) if wm2 else 300
            if desc:
                new_entries.append(make_placeholder(w, 200) + " " + desc)
            else:
                new_entries.append(make_placeholder(w, 200))
        else:
            new_entries.append(entry)

    if not needs_replace:
        return tag

    new_srcset = ', '.join(new_entries)
    old_srcset = 'srcset=' + srcset_m.group(1) + srcset_m.group(2) + srcset_m.group(1)
    new_srcset_attr = 'srcset=' + srcset_m.group(1) + new_srcset + srcset_m.group(1)
    tag = tag.replace(old_srcset, new_srcset_attr)
    total_replaced += 1
    return tag

content = source_pattern.sub(process_source, content)

# ============================================================
# 3. <video> poster
# ============================================================
video_pattern = re.compile(r'<video\b[^>]*>', re.DOTALL)

def process_video(match):
    global total_replaced
    tag = match.group(0)

    poster_m = re.search(r'poster=(["\'])(.+?)\1', tag)
    if not poster_m or not should_process(poster_m.group(2)):
        return tag

    poster = poster_m.group(2)
    w, h = get_placeholder_dimensions(tag, 640, 360)
    placeholder = make_placeholder(w, h)

    # Remove old data-original-poster
    tag = re.sub(r'\s*data-original-poster=(["\'])(.+?)\1', '', tag)

    old_poster = 'poster=' + poster_m.group(1) + poster + poster_m.group(1)
    new_poster = 'poster=' + poster_m.group(1) + placeholder + poster_m.group(1) + ' data-original-poster=' + poster_m.group(1) + poster + poster_m.group(1)
    tag = tag.replace(old_poster, new_poster, 1)
    total_replaced += 1
    return tag

content = video_pattern.sub(process_video, content)

# ============================================================
# 4. data-bg, data-lazyload, data-src on any element
# ============================================================
data_attr_pattern = re.compile(
    r'\s(data-(?:bg|lazyload|src|bg-image))=(["\'])([^"\']+)\2'
)

def process_data_attr(match):
    global total_replaced
    attr_name = match.group(1)
    quote = match.group(2)
    url = match.group(3)

    if not should_process(url):
        return match.group(0)

    w, h = 1200, 800
    placeholder = make_placeholder(w, h)

    orig_attr = 'data-original-' + attr_name.replace('data-', '')

    old_attr = attr_name + '=' + quote + url + quote
    new_attr = attr_name + '=' + quote + placeholder + quote + ' ' + orig_attr + '=' + quote + url + quote
    total_replaced += 1
    return ' ' + new_attr

content = data_attr_pattern.sub(process_data_attr, content)

# ============================================================
# 5. CSS url() in inline style="..." attributes
# ============================================================
style_attr_pattern = re.compile(
    r'(style=(["\'])[^"\']*?)url\((["\']?)(https?://[^"\')]+|[^"\')]+\.(?:jpg|jpeg|png|gif|webp|svg))(?:\3)([^"\']*?\2)',
    re.IGNORECASE | re.DOTALL
)

def process_style_attr(match):
    global total_replaced
    prefix = match.group(1)
    open_q = match.group(3)
    url = match.group(4)
    suffix = match.group(5)

    if not should_process(url):
        return match.group(0)

    placeholder = make_placeholder(1200, 800)
    total_replaced += 1

    old_url = 'url(' + open_q + url + open_q + ')'
    new_url = 'url(' + open_q + placeholder + open_q + ')'
    return match.group(0).replace(old_url, new_url)

content = style_attr_pattern.sub(process_style_attr, content)

# ============================================================
# 6. CSS url() in <style> blocks
# ============================================================
style_block_pattern = re.compile(r'<style[^>]*>.*?</style>', re.DOTALL)

def process_style_block(match):
    global total_replaced
    block = match.group(0)

    url_pattern = re.compile(r'url\([\"\']?([^\"\')]+)[\"\']?\)')

    def replace_url_in_block(url_match):
        global total_replaced
        url = url_match.group(1)
        if not should_process(url):
            return url_match.group(0)
        placeholder = make_placeholder(1200, 800)
        total_replaced += 1
        return 'url(' + placeholder + ')'

    new_block = url_pattern.sub(replace_url_in_block, block)
    return new_block

content = style_block_pattern.sub(process_style_block, content)

# ============================================================
# Write back
# ============================================================
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Total image references replaced: " + str(total_replaced))
print()
for d in details[:40]:
    print(d)
if len(details) > 40:
    print("  ... and " + str(len(details) - 40) + " more")

# ============================================================
# Verify
# ============================================================
print()
print("=== VERIFICATION ===")
with open(FILE, encoding='utf-8') as f:
    content = f.read()

img_tags = re.findall(r'<img\b[^>]*>', content, re.DOTALL)
real_imgs = 0
placeholder_imgs = 0
excluded_imgs = 0
for t in img_tags:
    src_m = re.search(r'\ssrc=(["\'])(.+?)\1', t)
    if src_m:
        src = src_m.group(2)
        if 'placehold.co' in src:
            placeholder_imgs += 1
        elif any(excl in src for excl in EXCLUDE_PATTERNS):
            excluded_imgs += 1
        elif src.startswith('data:'):
            pass
        else:
            real_imgs += 1
            print("  STILL REAL img: " + src[:80])

print("<img>: " + str(len(img_tags)) + " | Placeholder: " + str(placeholder_imgs) + " | Excluded: " + str(excluded_imgs) + " | Still real: " + str(real_imgs))

retinas = re.findall(r'data-retina="([^"]+)"', content)
real_retinas = [r for r in set(retinas) if 'placehold.co' not in r and 'jainheritageschool' in r]
print("data-retina real: " + str(len(real_retinas)))

data_bgs = re.findall(r'data-bg="([^"]+)"', content)
real_bgs = [b for b in data_bgs if 'placehold.co' not in b and 'jainheritageschool' in b]
print("data-bg real: " + str(len(real_bgs)))

css_urls = re.findall(r'url\([\"\']?([^\"\')]+)[\"\']?\)', content)
real_css = [u for u in css_urls if 'jainheritageschool' in u and 'placehold.co' not in u]
print("CSS url() real: " + str(len(real_css)))

posters = re.findall(r'poster="([^"]+)"', content)
real_posters = [p for p in posters if 'jainheritageschool' in p and 'placehold.co' not in p]
print("video poster real: " + str(len(real_posters)))

total_placeholders = content.count('placehold.co')
total_originals = content.count('data-original-src=')
print()
print("Total placehold.co URLs: " + str(total_placeholders))
print("Total data-original-src preserved: " + str(total_originals))
