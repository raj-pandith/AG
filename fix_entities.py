#!/usr/bin/env python3
"""Fix double-encoded HTML entities in data-settings attributes."""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com")

def process_file(filepath):
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return 0

    original = content
    count = 0

    # Match data-settings attributes and fix double-encoded entities
    pattern = re.compile(r'data-settings="(.*?)"', re.DOTALL)

    def fix_entities(m):
        nonlocal count
        attr_value = m.group(1)
        if '&amp;quot;' in attr_value:
            attr_value = attr_value.replace('&amp;quot;', '&quot;')
            count += 1
            return f'data-settings="{attr_value}"'
        return m.group(0)

    content = pattern.sub(fix_entities, content)

    if content != original:
        filepath.write_text(content, encoding='utf-8')

    return count


def main():
    total = 0
    for root, dirs, files in os.walk(BASE):
        for fname in files:
            if not fname.endswith('.html'):
                continue
            filepath = Path(root) / fname
            count = process_file(filepath)
            if count > 0:
                total += count
                print(f"  {filepath.relative_to(BASE)} — fixed {count} attributes")

    print(f"\nDone! Fixed {total} double-encoded attributes.")


if __name__ == "__main__":
    main()
