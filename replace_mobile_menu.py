"""
Replace mobile menu in all HTML files with the reference menu from mainfolder.com/index.html.
"""
import os
import re

base_dir = r"c:\My Web Sites\Jain2"

# Read the reference mobile menu block from mainfolder.com/index.html
ref_file = os.path.join(base_dir, "mainfolder.com", "index.html")
with open(ref_file, "r", encoding="utf-8") as f:
    ref_content = f.read()

# Extract the mobile menu block from the reference file
# Pattern: from <!--==============================Mobile Menu============================== --> to closing </div> of th-menu-wrapper
mobile_menu_pattern = re.compile(
    r'<!--\s*=+\s*Mobile Menu\s*=+\s*-->\s*\n'
    r'\s*<div class="th-menu-wrapper onepage-nav">.*?\n\s*</div>\s*\n',
    re.DOTALL
)

match = mobile_menu_pattern.search(ref_content)
if not match:
    print("ERROR: Could not find mobile menu block in reference file!")
    exit(1)

new_mobile_menu = match.group(0).rstrip('\n')
print(f"Found reference mobile menu block ({len(new_mobile_menu)} chars)")
print(f"Last 100 chars: ...{new_mobile_menu[-100:]}")

# Now process all HTML files in both mainfolder.com and ag.com
for site in ["mainfolder.com", "ag.com"]:
    site_dir = os.path.join(base_dir, site)
    print(f"\nProcessing {site}...")

    # Find all HTML files (excluding assets directories)
    html_files = []
    for root, dirs, files in os.walk(site_dir):
        # Skip assets directories
        dirs[:] = [d for d in dirs if d not in ('assets', 'cdn', 'cdnjs', 'hts-cache')]
        for fname in files:
            if fname.endswith('.html'):
                html_files.append(os.path.join(root, fname))

    print(f"  Found {len(html_files)} HTML files")

    updated_count = 0
    skipped_count = 0
    error_count = 0

    for filepath in sorted(html_files):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Check if the file has the mobile menu block
            if not mobile_menu_pattern.search(content):
                skipped_count += 1
                continue

            # Replace the mobile menu block
            new_content = mobile_menu_pattern.sub(new_mobile_menu, content)

            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                rel_path = os.path.relpath(filepath, site_dir)
                print(f"  Updated: {rel_path}")
                updated_count += 1
            else:
                skipped_count += 1

        except Exception as e:
            error_count += 1
            print(f"  ERROR: {os.path.relpath(filepath, site_dir)}: {e}")

    print(f"  Summary for {site}: {updated_count} updated, {skipped_count} skipped, {error_count} errors")

print("\nDone!")