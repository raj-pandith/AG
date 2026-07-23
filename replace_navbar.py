#!/usr/bin/env python3
"""
Replace the navbar (header section) in all HTML files with the navbar from index.html.
"""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com")
EXCLUDE_DIRS = {"admissions-2026-27"}

# Read the source navbar from index.html
INDEX_FILE = BASE / "index.html"
index_content = INDEX_FILE.read_text(encoding='utf-8', errors='replace')

# Extract the header from index.html
header_start_marker = '<header class="th-header header-layout1">'
header_end_marker = '</header>'

header_start = index_content.find(header_start_marker)
header_end = index_content.find(header_end_marker, header_start) + len(header_end_marker)

if header_start == -1 or header_end < header_start:
    print("ERROR: Could not find header in index.html")
    exit(1)

source_header = index_content[header_start:header_end]
print(f"Source header extracted: {len(source_header)} chars")
print(f"Header starts with: {source_header[:80]}...")
print(f"Header ends with: ...{source_header[-80:]}")


def replace_header(content):
    """Replace the header in content with the source header from index.html."""
    # Find the header in this file
    start = content.find(header_start_marker)
    if start == -1:
        return content, False

    end = content.find(header_end_marker, start) + len(header_end_marker)
    if end < start:
        return content, False

    # Replace
    new_content = content[:start] + source_header + content[end:]
    return new_content, True


def fix_duplicate_permissions(content):
    """Remove duplicate Permissions-Policy meta tags, keeping only one."""
    # Count occurrences
    count = content.count('<meta http-equiv="Permissions-Policy" content="interest-cohort=()">')
    if count <= 1:
        return content, False

    # Remove all occurrences
    content = content.replace('<meta http-equiv="Permissions-Policy" content="interest-cohort=()">\n', '')
    content = content.replace('<meta http-equiv="Permissions-Policy" content="interest-cohort=()">', '')

    # Add one after the charset meta tag
    charset_pattern = re.compile(r'(<meta charset="utf-8">\s*\n)')

    def add_perm_policy(m):
        return m.group(1) + '    <meta http-equiv="Permissions-Policy" content="interest-cohort=()">\n'

    content = charset_pattern.sub(add_perm_policy, content)
    return content, True


def process_file(filepath):
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  SKIP (read error): {filepath.name} — {e}")
        return False

    if filepath.suffix != '.html':
        return False

    # Skip index.html itself
    if filepath.name == 'index.html':
        return False

    changed = False

    # Replace header
    content, c = replace_header(content)
    changed |= c

    # Fix duplicate Permissions-Policy tags
    content, c = fix_duplicate_permissions(content)
    changed |= c

    if changed:
        filepath.write_text(content, encoding='utf-8')
        return True

    return False


def main():
    total = 0
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in sorted(files):
            if not fname.endswith('.html'):
                continue
            filepath = Path(root) / fname
            if process_file(filepath):
                total += 1
                print(f"  {filepath.relative_to(BASE)} — navbar replaced")
    print(f"\nDone! Replaced navbar in {total} pages.")


if __name__ == "__main__":
    main()
