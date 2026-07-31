"""
Fix broken viewport meta tag in all HTML files.
The viewport meta contains lorem ipsum text instead of the proper directive.
"""
import os
import re

base_dir = r"c:\My Web Sites\Jain2"
sites = ["mainfolder.com", "ag.com"]

# The broken viewport pattern (with lorem ipsum) - handles both attribute orders
broken_pattern = re.compile(
    r'<meta\s+(?:name="viewport"\s+content="|content="[^"]*?"\s+name="viewport")[^>]*>',
    re.IGNORECASE
)

# The correct replacement
correct_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'

total_fixed = 0
total_skipped = 0

for site in sites:
    site_dir = os.path.join(base_dir, site)
    print(f"\nProcessing {site}...")

    fixed_count = 0
    skipped_count = 0

    # Walk through all HTML files in the site directory
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

                # Check if file has the broken viewport meta
                if broken_pattern.search(content):
                    # Replace the broken meta tag
                    new_content = broken_pattern.sub(correct_meta, content)

                    # Write the updated content
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    rel_path = os.path.relpath(filepath, site_dir)
                    print(f"  [OK] Fixed: {rel_path}")
                    fixed_count += 1
                else:
                    skipped_count += 1

            except Exception as e:
                print(f"  [ERR] ERROR: {os.path.relpath(filepath, site_dir)}: {e}")

    print(f"  Summary: {fixed_count} fixed, {skipped_count} skipped")
    total_fixed += fixed_count
    total_skipped += skipped_count

print(f"\n{'='*60}")
print(f"TOTAL: {total_fixed} files fixed, {total_skipped} files skipped")
print(f"{'='*60}")
