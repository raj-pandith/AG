#!/usr/bin/env python3
"""
Truncate all navbar texts and their inner texts to a maximum of 2 words per link.
Handles &amp; connectors properly (not counted as separate words).
"""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com")
EXCLUDE_DIRS = {"admissions-2026-27"}

# Pattern to match <a>TEXT</a> (single or multi-line TEXT without nested tags)
A_TAG_RE = re.compile(r'(<a\s+[^>]*>)([^<]+)(</a>)', re.DOTALL)

# Pattern to match widget titles
WIDGET_TITLE_RE = re.compile(r'(<h3 class="widget_title">)([^<]+)(</h3>)')

# CTA button pattern
CTA_RE = re.compile(
    r'(<a\s+href="admissions-2026-27[^"]*"\s+target="_blank"\s+class="th-btn\s+blue-btn\s+th-icon">)([^<]+)(<i)',
    re.DOTALL
)


def truncate_words(text, max_words=2):
    """Truncate text, treating &amp;/& as a connector, not a separate word."""
    normalized = text.replace('&amp;', ' & ')
    words = [w for w in normalized.split() if w not in ('&', '&amp;')]
    if len(words) > max_words:
        return ' '.join(words[:max_words]) + '.'
    return text


def truncate_a_tags(html):
    """Truncate all <a>TEXT</a> link texts to 2 words. Returns (new_html, changed)."""
    changed = False

    def repl(m):
        nonlocal changed
        prefix, text, suffix = m.group(1), m.group(2).strip(), m.group(3)
        if not text.strip() or not any(c.isalpha() for c in text):
            return m.group(0)
        new_text = truncate_words(text, 2)
        if new_text != text:
            changed = True
        return prefix + new_text + suffix

    new_html = A_TAG_RE.sub(repl, html)
    return new_html, changed


def truncate_widget_titles(html):
    """Truncate <h3 class="widget_title">TEXT</h3> to 2 words. Returns (new_html, changed)."""
    changed = False

    def repl(m):
        nonlocal changed
        prefix, text, suffix = m.group(1), m.group(2).strip(), m.group(3)
        new_text = truncate_words(text, 2)
        if new_text != text:
            changed = True
        return prefix + new_text + suffix

    new_html = WIDGET_TITLE_RE.sub(repl, html)
    return new_html, changed


def fix_cta_button(html):
    """Fix CTA button text. Returns (new_html, changed)."""
    changed = False

    def repl(m):
        nonlocal changed
        prefix, text, suffix = m.group(1), m.group(2).strip(), m.group(3)
        new_text = truncate_words(text, 2)
        if new_text != text:
            changed = True
        return prefix + new_text + suffix

    new_html = CTA_RE.sub(repl, html)
    return new_html, changed


def process_navbar(html):
    """Process all navbar regions. Returns (new_html, changed)."""
    result = html
    any_changed = False

    # === Header area ===
    header_re = re.compile(r'(<header\b[^>]*>)(.*?)(</header>)', re.DOTALL)
    header_match = header_re.search(result)
    if header_match:
        prefix_h, inner, suffix_h = header_match.group(1), header_match.group(2), header_match.group(3)
        inner_changed = False

        # CTA button first (before general <a> truncation)
        inner, c = fix_cta_button(inner)
        inner_changed |= c

        # Then all <a> tags
        inner, c = truncate_a_tags(inner)
        inner_changed |= c

        if inner_changed:
            any_changed = True
            result = prefix_h + inner + suffix_h

    # === Footer ===
    footer_re = re.compile(r'(<footer\b[^>]*>)(.*?)(</footer>)', re.DOTALL)
    footer_match = footer_re.search(result)
    if footer_match:
        prefix_f, inner, suffix_f = footer_match.group(1), footer_match.group(2), footer_match.group(3)
        inner_changed = False

        # Widget titles
        inner, c = truncate_widget_titles(inner)
        inner_changed |= c

        # Footer <a> links
        inner, c = truncate_a_tags(inner)
        inner_changed |= c

        if inner_changed:
            any_changed = True
            result = prefix_f + inner + suffix_f

    return result, any_changed


def process_file(filepath):
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  SKIP (read error): {filepath.name} — {e}")
        return False

    if filepath.suffix != '.html':
        return False

    new_content, changed = process_navbar(content)

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
