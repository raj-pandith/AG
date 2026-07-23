#!/usr/bin/env python3
"""
Replace image URLs inside Elementor data-settings JSON attributes.
Handles: data-settings="{...background_slideshow_gallery:[{url:"..."}]...}"
Also handles: data-settings="{...background_background: slideshow, background_slideshow_gallery:[...]...}"
"""

import os
import re
import json
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com")
PLACEHOLDER_PREFIX = "https://placehold.co"
EXCLUDE_DIRS = set()


def get_dim_from_url(url):
    """Extract dimensions from a URL like JHS-Banner-LP-006.jpg (no dims) or 1024x576."""
    # Check for explicit WxH in the URL
    m = re.search(r'/(\d{2,4})x(\d{2,4})/', url)
    if m:
        return int(m.group(1)), int(m.group(2))

    # Check filename for dimensions
    basename = url.split('/')[-1].split('?')[0]
    m = re.search(r'[_\-](\d{2,4})[xX×](\d{2,4})', basename)
    if m:
        return int(m.group(1)), int(m.group(2))

    # Known patterns for banner/slider images
    if 'banner' in url.lower() or 'banner' in basename.lower():
        return 1920, 800
    if 'hero' in url.lower() or 'hero' in basename.lower():
        return 1920, 800

    # Default for slideshow images
    return 1920, 800


def process_file(filepath):
    """Process a single HTML file, replacing image URLs in data-settings JSON."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  SKIP (read error): {filepath} — {e}")
        return 0

    original = content
    replacements = 0

    # Pattern: find data-settings attribute containing background_slideshow_gallery
    # The value is HTML-entity-encoded JSON that may contain nested braces (arrays)
    pattern = re.compile(
        r'(data-settings\s*=\s*")(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})"',
        re.IGNORECASE
    )

    def replace_gallery(m):
        nonlocal replacements
        prefix = m.group(1)  # data-settings="
        json_str = m.group(2)  # the JSON object

        # Check if already processed
        if 'data-original-gallery-urls' in json_str or 'placehold.co' in json_str:
            return m.group(0)

        try:
            # Decode HTML entities
            json_str = json_str.replace('&quot;', '"').replace('&#039;', "'").replace('&amp;', '&')

            data = json.loads(json_str)

            gallery = data.get('background_slideshow_gallery', [])
            if not gallery:
                return m.group(0)

            original_urls = []
            for slide in gallery:
                if 'url' in slide:
                    original_urls.append(slide['url'])
                    w, h = get_dim_from_url(slide['url'])
                    slide['url'] = f"{PLACEHOLDER_PREFIX}/{w}x{h}"

            if not original_urls:
                return m.group(0)

            # Re-encode back to HTML entities (only quote chars, not & in URLs)
            new_json = json.dumps(data, ensure_ascii=False)
            # Encode quotes for HTML attribute context
            new_json = new_json.replace('"', '&quot;').replace("'", '&#039;')

            # Add original URLs as a separate attribute
            result = prefix + new_json + '"'
            original_urls_json = json.dumps(original_urls, ensure_ascii=False)
            original_urls_escaped = original_urls_json.replace('"', '&quot;')
            result += f' data-original-gallery-urls="{original_urls_escaped}"'

            replacements += len(original_urls)
            return result

        except (json.JSONDecodeError, KeyError) as e:
            print(f"  WARN: Could not parse JSON in {filepath}: {e}")
            return m.group(0)

    content = pattern.sub(replace_gallery, content)

    if content != original:
        filepath.write_text(content, encoding='utf-8')

    return replacements


def main():
    total_files = 0
    total_imgs = 0

    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for fname in files:
            if not fname.endswith('.html'):
                continue
            filepath = Path(root) / fname
            count = process_file(filepath)
            if count > 0:
                total_files += 1
                total_imgs += count
                print(f"  {filepath.relative_to(BASE)} — {count} gallery images replaced")

    print(f"\nDone! Replaced {total_imgs} gallery URLs across {total_files} files.")


if __name__ == "__main__":
    main()
