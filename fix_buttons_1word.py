#!/usr/bin/env python3
"""
Truncate ALL button texts (class="th-btn") to a maximum of 1 word across all pages.
Processes matches in reverse to avoid position shifting.
"""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com")
EXCLUDE_DIRS = {"admissions-2026-27"}


def truncate_to_one_word(text):
    """Truncate text to 1 word and add period."""
    words = text.split()
    if len(words) > 1:
        return words[0] + '.'
    return text


def process_html(content):
    """Truncate all th-btn button texts to 1 word. Returns (new_content, changed)."""
    # Find all th-btn occurrences and their text
    pattern = re.compile(r'class="th-btn[^"]*"[^>]*>([^<]+)')
    matches = list(pattern.finditer(content))

    if not matches:
        return content, False

    changed = False
    result = content

    # Process from end to start to avoid position shifting
    for m in reversed(matches):
        text = m.group(1).strip()
        new_text = truncate_to_one_word(text)
        if new_text != text:
            changed = True
            result = result[:m.start(1)] + new_text + result[m.end(1):]

    return result, changed


def process_file(filepath):
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  SKIP (read error): {filepath.name} — {e}")
        return False

    if filepath.suffix != '.html':
        return False

    new_content, changed = process_html(content)

    if changed:
        filepath.write_text(new_content, encoding='utf-8')
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
                print(f"  {filepath.relative_to(BASE)} — truncated")
    print(f"\nDone! Fixed {total} pages.")


if __name__ == "__main__":
    main()
