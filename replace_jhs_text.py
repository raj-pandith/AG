"""
Replace visible JHS/jhs text with AG/ag across HTML files.
Scope: alt attributes, meta content attributes, and visible text.
Excludes: JS function names, CSS variables/selectors, URLs, social handles.
"""
import os
import re

base_dir = r"c:\My Web Sites\Jain2"

# Process both sites, excluding admissions subdirectories
for site in ["mainfolder.com", "ag.com"]:
    site_dir = os.path.join(base_dir, site)
    print(f"\nProcessing {site}...")

    html_files = []
    for root, dirs, files in os.walk(site_dir):
        # Skip admissions and assets subdirectories
        dirs[:] = [d for d in dirs if d not in ('assets', 'cdn', 'cdnjs', 'hts-cache', 'admissions-2026-27', 'ojix-work')]
        for fname in files:
            if fname.endswith('.html'):
                html_files.append(os.path.join(root, fname))

    print(f"  Found {len(html_files)} HTML files")

    updated_count = 0
    skipped_count = 0

    for filepath in sorted(html_files):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Check if file contains jhs (case-insensitive)
            if not re.search(r'\bjhs\b', content, re.IGNORECASE):
                skipped_count += 1
                continue

            # Apply replacements (case-insensitive where appropriate)
            new_content = content

            # 1. Replace in alt attributes: alt="jhs" or alt='jhs' (case-insensitive)
            new_content = re.sub(r'(alt=["\'])\s*jhs\s*(["\'])', lambda m: m.group(1) + 'ag' + m.group(2), new_content, flags=re.IGNORECASE)

            # 2. Replace in meta content attributes: content="jhs" or content='jhs' (case-insensitive)
            new_content = re.sub(r'(content=["\'])\s*jhs\s*(["\'])', lambda m: m.group(1) + 'ag' + m.group(2), new_content, flags=re.IGNORECASE)

            # 3. Replace visible text "JHS" or "jhs" but NOT inside:
            #    - HTML tags/attributes (already handled above)
            #    - URLs (http://, /path/, etc.)
            #    - JavaScript (inside <script> tags)
            #    - CSS/IDs/classes
            #    - Function names and callback parameters

            # Strategy: replace standalone "JHS" or "jhs" word outside of tags, scripts, and URLs
            # First, protect content inside <script>...</script> and inline styles
            script_placeholders = {}

            def protect_scripts_and_styles(match):
                key = f"__PROTECTED_{len(script_placeholders)}__"
                script_placeholders[key] = match.group(0)
                return key

            # Protect <script>...</script> blocks
            new_content = re.sub(r'<script\b[^>]*>.*?</script>', protect_scripts_and_styles, new_content, flags=re.DOTALL | re.IGNORECASE)
            # Protect <style>...</style> blocks
            new_content = re.sub(r'<style\b[^>]*>.*?</style>', protect_scripts_and_styles, new_content, flags=re.DOTALL | re.IGNORECASE)
            # Protect inline style attributes
            new_content = re.sub(r'\sstyle="[^"]*"', protect_scripts_and_styles, new_content, flags=re.IGNORECASE)

            # Replace standalone "jhs" word (case-insensitive) in remaining text
            # This catches visible text like "Join the JHS Family" or "Life at JHS"
            new_content = re.sub(r'\bjhs\b', 'ag', new_content, flags=re.IGNORECASE)

            # Restore protected content
            for key, value in script_placeholders.items():
                new_content = new_content.replace(key, value)

            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                rel_path = os.path.relpath(filepath, site_dir)
                print(f"  Updated: {rel_path}")
                updated_count += 1
            else:
                skipped_count += 1

        except Exception as e:
            print(f"  ERROR: {os.path.relpath(filepath, site_dir)}: {e}")

    print(f"  Summary for {site}: {updated_count} updated, {skipped_count} skipped")

print("\nDone!")