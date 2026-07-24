#!/usr/bin/env python3
"""Replace all images with placeholders in application/index.html"""

import re
from pathlib import Path

FILE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com\admissions-2026-27\application\index.html")

with open(FILE, encoding='utf-8') as f:
    content = f.read()

total_replaced = 0
details = []

EXCLUDE_PATTERNS = ['placehold.co', 'ytimg.com', 'gravatar.com', 'w.org']

def should_process(url):
    if not url or url.startswith('data:'):
        return False
    if any(excl in url for excl in EXCLUDE_PATTERNS):
        return False
    return 'jainheritageschool' in url or re.search(r'\.(jpg|jpeg|png|gif|webp|svg|bmp|ico)(\?|#|$)', url, re.IGNORECASE)

def get_dims(tag, dw=300, dh=200):
    w, h = dw, dh
    wm = re.search(r'width=(["\']?)(\d+)\1', tag)
    hm = re.search(r'height=(["\']?)(\d+)\1', tag)
    if wm: w = int(wm.group(2))
    if hm: h = int(hm.group(2))
    return w, h

def ph(w, h):
    return "https://placehold.co/" + str(w) + "x" + str(h)

# 1. <img> tags
img_pattern = re.compile(r'<img\b[^>]*>', re.DOTALL)

def process_img(match):
    global total_replaced
    tag = match.group(0)

    src_m = re.search(r'\ssrc=(["\'])(.+?)\1', tag)
    if not src_m:
        return tag

    src = src_m.group(2)
    quote = src_m.group(1)

    if 'placehold.co' in src or not should_process(src):
        return tag

    w, h = get_dims(tag)
    original = src

    if src.startswith('data:image/svg'):
        lazy_m = re.search(r'data-lazy-src=(["\'])(.+?)\1', tag)
        if lazy_m and should_process(lazy_m.group(2)):
            original = lazy_m.group(2)
        else:
            return tag

    p = ph(w, h)

    tag = re.sub(r'\s*data-original-src=(["\'])(.+?)\1', '', tag)

    old_src = 'src=' + quote + src + quote
    new_src = 'src=' + quote + p + quote + ' data-original-src=' + quote + original + quote
    tag = tag.replace(old_src, new_src, 1)

    lazy_m = re.search(r'data-lazy-src=(["\'])(.+?)\1', tag)
    if lazy_m and should_process(lazy_m.group(2)):
        old = 'data-lazy-src=' + lazy_m.group(1) + lazy_m.group(2) + lazy_m.group(1)
        tag = tag.replace(old, 'data-lazy-src=' + lazy_m.group(1) + p + lazy_m.group(1))

    data_src_m = re.search(r'data-src=(["\'])(.+?)\1', tag)
    if data_src_m and should_process(data_src_m.group(2)):
        old = 'data-src=' + data_src_m.group(1) + data_src_m.group(2) + data_src_m.group(1)
        tag = tag.replace(old, 'data-src=' + data_src_m.group(1) + p + data_src_m.group(1))

    retina_m = re.search(r'data-retina=(["\'])(.+?)\1', tag)
    if retina_m and should_process(retina_m.group(2)):
        old = 'data-retina=' + retina_m.group(1) + retina_m.group(2) + retina_m.group(1)
        tag = tag.replace(old, 'data-retina=' + retina_m.group(1) + p + retina_m.group(1))

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
                    new_entries.append(ph(ew, h) + " " + desc)
                else:
                    new_entries.append(entry)
            else:
                if should_process(entry):
                    new_entries.append(ph(w, h))
                else:
                    new_entries.append(entry)
        new_srcset = ', '.join(new_entries)
        old_srcset = 'srcset=' + srcset_m.group(1) + srcset_m.group(2) + srcset_m.group(1)
        new_srcset_attr = 'srcset=' + srcset_m.group(1) + new_srcset + srcset_m.group(1)
        tag = tag.replace(old_srcset, new_srcset_attr)

    total_replaced += 1
    details.append("img: " + original[:60])
    return tag

content = img_pattern.sub(process_img, content)

# 2. <source> tags
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
                new_entries.append(ph(w, 200) + " " + desc)
            else:
                new_entries.append(ph(w, 200))
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

# 3. data-bg
data_bg_pattern = re.compile(r'\s(data-bg)=(["\'])([^"\']+)\2')

def process_data_bg(match):
    global total_replaced
    quote = match.group(2)
    url = match.group(3)

    if not should_process(url):
        return match.group(0)

    p = ph(1200, 800)
    total_replaced += 1
    return ' data-bg=' + quote + p + quote

content = data_bg_pattern.sub(process_data_bg, content)

# 4. data-src, data-lazyload, data-bg-image
data_attr_pattern = re.compile(r'\s(data-(?:lazyload|src|bg-image))=(["\'])([^"\']+)\2')

def process_data_attr(match):
    global total_replaced
    quote = match.group(2)
    url = match.group(3)

    if not should_process(url):
        return match.group(0)

    p = ph(1200, 800)
    total_replaced += 1
    return ' ' + match.group(1) + '=' + quote + p + quote

content = data_attr_pattern.sub(process_data_attr, content)

# 5. <video> poster
video_pattern = re.compile(r'<video\b[^>]*>', re.DOTALL)

def process_video(match):
    global total_replaced
    tag = match.group(0)

    poster_m = re.search(r'poster=(["\'])(.+?)\1', tag)
    if not poster_m or not should_process(poster_m.group(2)):
        return tag

    poster = poster_m.group(2)
    w, h = get_dims(tag, 640, 360)
    p = ph(w, h)

    tag = re.sub(r'\s*data-original-poster=(["\'])(.+?)\1', '', tag)
    old_poster = 'poster=' + poster_m.group(1) + poster + poster_m.group(1)
    new_poster = 'poster=' + poster_m.group(1) + p + poster_m.group(1) + ' data-original-poster=' + poster_m.group(1) + poster + poster_m.group(1)
    tag = tag.replace(old_poster, new_poster, 1)
    total_replaced += 1
    return tag

content = video_pattern.sub(process_video, content)

# 6. CSS url() in inline styles
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

    p = ph(1200, 800)
    total_replaced += 1
    old_url = 'url(' + open_q + url + open_q + ')'
    new_url = 'url(' + open_q + p + open_q + ')'
    return match.group(0).replace(old_url, new_url)

content = style_attr_pattern.sub(process_style_attr, content)

# 7. CSS url() in <style> blocks
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
        p = ph(1200, 800)
        total_replaced += 1
        return 'url(' + p + ')'

    return url_pattern.sub(replace_url_in_block, block)

content = style_block_pattern.sub(process_style_block, content)

# Write back
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Total image references replaced: " + str(total_replaced))
print()
for d in details[:40]:
    print("  " + d)
if len(details) > 40:
    print("  ... and " + str(len(details) - 40) + " more")

# Verify
print()
print("=== VERIFICATION ===")
with open(FILE, encoding='utf-8') as f:
    vcontent = f.read()

img_tags = re.findall(r'<img\b[^>]*>', vcontent, re.DOTALL)
real_imgs = 0
placeholder_imgs = 0
for t in img_tags:
    src_m = re.search(r'\ssrc=(["\'])(.+?)\1', t)
    if src_m:
        src = src_m.group(2)
        if 'placehold.co' in src:
            placeholder_imgs += 1
        elif any(excl in src for excl in EXCLUDE_PATTERNS):
            pass
        elif src.startswith('data:'):
            pass
        else:
            real_imgs += 1
            print("  STILL REAL: " + src[:80])

print("<img>: " + str(len(img_tags)) + " | Placeholder: " + str(placeholder_imgs) + " | Still real: " + str(real_imgs))
print("Total placehold.co URLs: " + str(vcontent.count('placehold.co')))
print("Total data-original-src preserved: " + str(vcontent.count('data-original-src=')))
