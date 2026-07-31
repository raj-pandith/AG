"""
Add lazy loading attribute to images in HTML files.
Skips: hero images, logos, icons, and images that already have loading attribute.
"""
import os
import re

base_dir = r"c:\My Web Sites\Jain2"
sites = ["mainfolder.com", "ag.com"]

# Patterns to skip (hero images, logos, icons, already lazy-loaded)
skip_patterns = [
    r'favicon',               # Favicon
    r'sprite',                # SVG sprites
]

# Keywords that indicate hero/above-fold images (skip lazy loading)
hero_keywords = ['hero', 'banner', 'logo']

total_updated = 0
total_skipped = 0

for site in sites:
    site_dir = os.path.join(base_dir, site)
    print(f"\nProcessing {site}...")

    updated_count = 0
    skipped_count = 0

    # Walk through all HTML files
    for root, dirs, files in os.walk(site_dir):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ('assets', 'cdn', 'cdnjs', 'hts-cache', 'admissions-2026-27', 'ojix-work')]

        for filename in files:
            if not filename.endswith('.html'):
                continue

            filepath = os.path.join(root, filename)

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find all <img> tags
                img_pattern = re.compile(r'<img\s[^>]*>', re.IGNORECASE)
                img_tags = img_pattern.findall(content)

                if not img_tags:
                    skipped_count += 1
                    continue

                modified = False
                new_content = content

                for img_tag in img_tags:
                    # Skip if already has loading attribute
                    if 'loading=' in img_tag:
                        continue

                    # Skip if matches skip patterns
                    should_skip = False
                    for pattern in skip_patterns:
                        if re.search(pattern, img_tag, re.IGNORECASE):
                            should_skip = True
                            break

                    if should_skip:
                        continue

                    # Skip hero/above-fold images (check src for keywords)
                    src_match = re.search(r'src\s*=\s*["\']([^"\']+)["\']', img_tag, re.IGNORECASE)
                    if src_match:
                        src = src_match.group(1).lower()
                        if any(keyword in src for keyword in hero_keywords):
                            continue

                    # Add loading="lazy" attribute
                    # Insert it after the src attribute
                    new_img_tag = re.sub(
                        r'(<img\s)',
                        r'\1loading="lazy" ',
                        img_tag,
                        count=1
                    )

                    if new_img_tag != img_tag:
                        new_content = new_content.replace(img_tag, new_img_tag, 1)
                        modified = True

                if modified:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    rel_path = os.path.relpath(filepath, site_dir)
                    print(f"  [OK] Updated: {rel_path}")
                    updated_count += 1
                else:
                    skipped_count += 1

            except Exception as e:
                print(f"  [ERR] ERROR: {os.path.relpath(filepath, site_dir)}: {e}")

    print(f"  Summary: {updated_count} updated, {skipped_count} skipped")
    total_updated += updated_count
    total_skipped += skipped_count

print(f"\n{'='*60}")
print(f"TOTAL: {total_updated} files updated, {total_skipped} files skipped")
print(f"{'='*60}")
