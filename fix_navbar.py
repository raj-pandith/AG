#!/usr/bin/env python3
"""
Fix navbar layout:
  1. Truncate CTA button text to max 5 words
  2. Truncate menu item text to max 20 words
  3. Ensure toggle button is OUTSIDE header-button div
"""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com")
EXCLUDE_DIRS = {"admissions-2026-27"}


def truncate_words(text, max_words):
    """Truncate text to max_words and add period."""
    words = text.split()
    if len(words) > max_words:
        return ' '.join(words[:max_words]) + '.'
    return text


def fix_navbar(content):
    changed = False

    # ====== FIX 1: Truncate CTA button text (Get In Touch button) ======
    # Pattern: <a href="..." class="th-btn blue-btn th-icon">TEXT<i class="fa-light fa-arrow-right-long"></i></a>
    cta_pattern = re.compile(
        r'(<a href="admissions-2026-27[^"]*" target="_blank" class="th-btn blue-btn th-icon">)([^<]+)(<i class="fa-light fa-arrow-right-long"></i></a>)',
        re.DOTALL
    )

    def fix_cta(match):
        nonlocal changed
        prefix = match.group(1)
        text = match.group(2).strip()
        suffix = match.group(3)

        new_text = truncate_words(text, 5)
        if new_text != text:
            changed = True
            return prefix + new_text + suffix
        return match.group(0)

    content = cta_pattern.sub(fix_cta, content)

    # ====== FIX 2: Truncate long menu items (> 20 words) ======
    menu_pattern = re.compile(
        r'(<a\s+href="[^"]*"\s+[^>]*>)([^<]{30,})(</a>)',
        re.DOTALL
    )

    def fix_menu(match):
        nonlocal changed
        prefix = match.group(1)
        text = match.group(2).strip()
        suffix = match.group(3)

        new_text = truncate_words(text, 20)
        if new_text != text:
            changed = True
            return prefix + new_text + suffix
        return match.group(0)

    content = menu_pattern.sub(fix_menu, content)

    # ====== FIX 3: Fix toggle button placement ======
    # Check if toggle button is inside header-button div (wrong)
    # It should be OUTSIDE the div
    toggle_pattern = re.compile(
        r'(<div class="header-button d-none d-xl-block">\s*'
        r'<!-- <button type="button" class="icon-btn[^>]*>\s*'
        r'<img[^>]*>\s*'
        r'</button> -->\s*'
        r'<a href="admissions-2026-27[^"]*" target="_blank" class="th-btn blue-btn th-icon">[^<]+</a>)\s*'
        r'(<button type="button" class="th-menu-toggle d-block d-xl-none">[^<]*</button>)\s*'
        r'(</div>)',
        re.DOTALL
    )

    def fix_toggle(match):
        nonlocal changed
        before_toggle = match.group(1)
        toggle = match.group(2)
        closing = match.group(3)

        # Move toggle OUTSIDE the div
        changed = True
        return before_toggle + '\n                            </div>\n                            ' + toggle + '\n                        </div>'

    content = toggle_pattern.sub(fix_toggle, content)

    # Also handle case where toggle is missing entirely (add it)
    if not changed:
        # Check if there's a header-button but no toggle after it
        header_btn_pattern = re.compile(
            r'(<div class="header-button d-none d-xl-block">\s*'
            r'<!-- <button type="button" class="icon-btn[^>]*>\s*'
            r'<img[^>]*>\s*'
            r'</button> -->\s*'
            r'<a href="admissions-2026-27[^"]*" target="_blank" class="th-btn blue-btn th-icon">[^<]+</a>)\s*'
            r'(</div>)\s*'
            r'(</div>\s*</div>\s*</div>\s*<div class="logo-bg)',
            re.DOTALL
        )

        def add_toggle(match):
            nonlocal changed
            btn_content = match.group(1)
            div_close = match.group(2)
            rest = match.group(3)

            changed = True
            return (btn_content + '\n                            </div>\n'
                    '                            <button type="button" class="th-menu-toggle d-block d-xl-none"><i class="far fa-bars"></i></button>\n'
                    '                        </div>\n                    </div>\n                </div>\n                <div class="logo-bg')

        content = header_btn_pattern.sub(add_toggle, content)

    return content, changed


def process_file(filepath):
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  SKIP (read error): {filepath.name} — {e}")
        return False

    if filepath.suffix != '.html':
        return False

    new_content, changed = fix_navbar(content)

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
                print(f"  {filepath.relative_to(BASE)} — navbar fixed")

    print(f"\nDone! Fixed navbar on {total} pages.")


if __name__ == "__main__":
    main()
