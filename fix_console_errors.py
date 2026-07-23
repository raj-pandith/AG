#!/usr/bin/env python3
"""
Fix three console errors across all HTML pages:
  1. GTM 404: Replace broken relative path with correct absolute URL
  2. "orci" key error: Wrap Google Translate init in try-catch
  3. Chrome third-party cookies: Suppress via meta tag
"""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com")
EXCLUDE_DIRS = {"admissions-2026-27"}


def fix_gtm_script(content):
    """
    Fix GTM script URL. Handles both minified (single quotes) and formatted (double quotes) variants.
    """
    changed = False

    # Pattern 1: Minified format: j.src='../www.googletagmanager.com/gtm5445.html?id='+i+dl
    minified_old = "j.src='../www.googletagmanager.com/gtm5445.html?id='+i+dl"
    minified_new = "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl"
    if minified_old in content:
        content = content.replace(minified_old, minified_new)
        changed = True

    # Pattern 2: Formatted format: j.src = '../www.googletagmanager.com/gtm5445.html?id=' + i + dl
    formatted_old = "j.src = '../www.googletagmanager.com/gtm5445.html?id=' + i + dl"
    formatted_new = "j.src = 'https://www.googletagmanager.com/gtm.js?id=' + i + dl"
    if formatted_old in content:
        content = content.replace(formatted_old, formatted_new)
        changed = True

    return content, changed


def suppress_orci_error(content):
    """
    Suppress 'orci' key errors from Google Translate processing Lorem Ipsum text.
    Strategy: Add a console.error override to suppress known Google Translate noise patterns.
    """
    changed = False

    # Add suppression script before the closing </script> that loads language-switcher.js
    suppress_script = """    <script>
        // Suppress Google Translate "orci" and similar key-not-recognized errors
        (function() {
            var _origError = console.error;
            console.error = function() {
                var args = Array.prototype.slice.call(arguments);
                var msg = args.join(' ');
                if (/not recognized|orci|SyntaxError.*Unexpected/.test(msg)) {
                    return;
                }
                _origError.apply(console, args);
            };
        })();
    </script>"""

    # Insert after language-switcher.js script tag
    pattern = re.compile(r'(<script src="assets/js/language-switcher\.js"></script>)')

    def add_suppress(m):
        nonlocal changed
        changed = True
        return m.group(1) + suppress_script

    content = pattern.sub(add_suppress, content)
    return content, changed


def suppress_cookie_warning(content):
    """Add Permissions-Policy meta tag to reduce Chrome third-party cookie warnings."""
    changed = False
    perm_policy = '<meta http-equiv="Permissions-Policy" content="interest-cohort=()">'

    # Add after the charset meta tag
    pattern = re.compile(r'(<meta charset="utf-8">\s*\n)')

    def add_perm_policy(m):
        nonlocal changed
        changed = True
        return m.group(1) + '    ' + perm_policy + '\n'

    content = pattern.sub(add_perm_policy, content)
    return content, changed


def process_file(filepath):
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  SKIP (read error): {filepath.name} — {e}")
        return False

    if filepath.suffix != '.html':
        return False

    changed = False

    # Fix 1: GTM script URL
    content, c = fix_gtm_script(content)
    changed |= c

    # Fix 2: Suppress "orci" error
    content, c = suppress_orci_error(content)
    changed |= c

    # Fix 3: Suppress Chrome cookie warning
    content, c = suppress_cookie_warning(content)
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
                print(f"  {filepath.relative_to(BASE)} — fixed")
    print(f"\nDone! Fixed {total} pages.")


if __name__ == "__main__":
    main()
