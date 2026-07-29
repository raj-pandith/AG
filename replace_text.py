#!/usr/bin/env python3
"""
Replace all visible text content with Lorem Ipsum while preserving:
  - Every HTML tag and its attributes/classes (font styling intact)
  - Whitespace, indentation, and formatting
  - data-original-src, data-original-bg-src attributes
  - Script logic, JSON data structures
  - Social media URLs and links

Replaces text in:
  - Regular HTML tags (headings, paragraphs, links, buttons, etc.)
  - Meta tag content attributes (description, keywords, og:title, etc.)
  - JSON-LD script content (name, description fields)
"""

import os
import re
import random
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\mainfolder.com")
EXCLUDE_DIRS = {"admissions-2026-27"}

_rng = random.Random(42)

LOREM_WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
    "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
    "velit", "esse", "cillum", "fugiat", "nulla", "pariatur", "excepteur", "sint",
    "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
    "deserunt", "mollit", "anim", "id", "est", "laborum", "porta", "semper",
    "purus", "facilisi", "nullam", "vehicula", "massa", "egestas", "sem", "augue",
    "viverra", "arcu", "felis", "bibendum", "urna", "congue", "quam", "pellentesque",
    "habitant", "morbi", "tristique", "senectus", "netus", "malesuada", "fames",
    "turpis", "egestas", "integer", "feugiat", "scelerisque", "varius", "morbi",
    "leo", "urna", "molestie", "at", "elementum", "eu", "facilisis", "sagittis",
    "phasellus", "vestibulum", "lorem", "blandit", "ultrices", "suscipit", "orci",
    "donec", "velit", "neque", "auctor", "blandit", "imperdiet", "sapien",
    "cras", "fermentum", "odio", "eu", "feugiat", "pretium", "nibh", "consequat",
    "quam", "vitae", "tortor", "condimentum", "lacinia", "eros", "donec", "ac",
    "dapibus", "ultrices", "iaculis", "nunc", "sed", "augue", "lacus", "congue",
    "felis", "donec", "et", "odio", "pellentesque", "diam", "volutpat", "commodo",
    "fringilla", "faucibus", "ornare", "nunc", "id", "cursus", "metus", "aliquam",
    "sodales", "proin", "pretium", "justo", "curabitur", "amet", "est", "quam",
    "porttitor", "magna", "gravida", "cum", "sociis", "natoque", "penatibus",
    "magnis", "dis", "parturient", "montes", "nascetur", "ridiculus", "mus",
    "mauris", "vitae", "ultricies", "integer", "quis", "auctor", "elit", "vulputate",
    "mi", "commodo", "euismod", "imperdiet", "massa", "tincidunt", "nulla",
    "maecenas", "porttitor", "massa", "pellentesque", "sodales", "proin",
    "sollicitudin", "curabitur", "libero", "vehicula", "nec", "mollis", "vel",
    "accumsan", "convallis", "nulla", "non", "nisi", "tempor", "facilisis",
    "egestas", "quisque", "eget", "diam", "blandit", "vel", "felis",
    "ullamcorper", "purus", "sit", "amet", "fermentum", "orci", "nisl", "semper",
    "nec", "sagittis", "sem", "leo", "ac", "tortor", "at", "pellentesque",
    "vitae", "congue", "eget", "posuere", "sem", "vitae", "interdum",
    "mattis", "suspendisse", "potenti", "vivamus", "augue", "laoreet",
    "cursus", "metus", "aliquam", "faucibus", "nunc", "varius", "pede",
    "interdum", "massa", "ut", "fermentum", "nam", "posuere", "sem",
    "mauris", "ullamcorper", "orci", "nisl", "eu", "semper", "sapien",
    "vestibulum", "ante", "ipsum", "primis", "in", "faucibus", "luctus",
    "posuere", "cubilia", "curae", "nullam", "vel", "nisi", "eu",
    "laoreet", "risus", "viverra", "accumsan", "a", "condimentum", "sem",
    "rutrum", "felis", "sed", "viverra", "nunc", "aliquet", "bibendum",
    "felis", "ornare", "tincidunt", "eros", "ut", "blandit", "turpis",
    "semper", "ut", "pharetra", "neque", "nunc", "sapien",
    "in", "sodales", "odio", "nec", "cras", "pellentesque",
    "ligula", "imperdiet", "suscipit",
    "felis", "malesuada", "velit", "tincidunt", "accumsan", "odio", "sodales",
    "at", "vestibulum", "nam", "cursus", "tellus", "ut", "ultricies", "lacus",
    "orci", "interdum", "et", "a", "class", "aptent", "taciti", "sociosqu",
    "litora", "torquent", "per", "conubia", "nostra", "inceptos", "hymenaeos",
    "sodales", "neque", "sed", "viverra", "donec", "iaculis", "congue", "semper",
    "hendrerit", "lectus", "a", "sodales", "quam", "tincidunt", "id", "faucibus",
    "laoreet", "odio", "condimentum", "etiam", "vel", "ligula", "eget", "nulla",
    "proin", "et", "nisi", "vel", "nunc", "posuere", "congue", "quam",
    "laoreet", "gravida", "hendrerit", "sapien", "et", "pellentesque",
    "sagittis", "viverra", "lacus", "sit", "amet", "nulla", "bibendum",
    "ullamcorper", "neque", "lobortis", "non", "consequat", "velit", "vitae",
    "tempor", "sem", "non", "suscipit", "sapien", "non", "massa", "a",
    "ultrices", "erat", "a", "commodo", "arcu", "vitae", "ornare", "dignissim",
    "varius", "quam", "mattis", "euismod", "facilisi", "phasellus", "libero",
    "condimentum", "iaculis", "a", "placerat", "nec", "nisl",
    "molestie", "erat", "eget", "consequat", "turpis", "semper",
    "vehicula", "sem", "vel", "tortor", "ornare", "tristique",
    "pulvinar", "eros", "non", "tincidunt", "felis", "ultricies", "iaculis",
    "morbi", "sed", "arcu", "vel", "sapien", "consequat",
    "hendrerit", "sed", "ac", "turpis", "consectetur", "adipiscing", "elit",
    "felis", "imperdiet", "orci",
    "fringilla", "quam", "efficitur", "velit", "vestibulum",
    "nec", "tincidunt", "nulla", "lacinia", "sodales",
    "pretium", "felis", "nec", "suscipit",
    "congue", "lectus", "a",
    "finibus", "tellus", "lobortis", "vel",
    "posuere", "semper", "sem", "non", "maximus",
    "faucibus", "elit", "ac", "dignissim",
    "placerat", "donec", "vitae", "tortor", "quis",
    "aliquet", "imperdiet", "diam", "vitae",
    "suscipit", "quam",
    "tempus", "nisl", "id", "urna", "consequat",
    "malesuada", "lacus", "eu", "congue",
    "dapibus", "odio", "accumsan", "tortor",
    "interdum", "nec", "congue", "nulla",
    "lobortis", "sapien", "vestibulum", "vitae", "ante",
    "blandit", "metus", "nisi", "non",
    "hendrerit", "quam", "cras", "posuere", "diam",
    "imperdiet", "consequat", "quisque", "ultricies",
    "nunc", "eu", "maximus", "sapien", "gravida",
    "at", "vestibulum", "velit", "mollis", "tincidunt",
    "quam", "nulla", "faucibus", "libero", "et",
    "imperdiet", "massa", "hendrerit",
    "nisi", "a", "fringilla", "felis", "mauris",
    "ac", "varius", "orci", "cras", "fermentum",
    "diam", "nec", "congue", "felis", "porttitor",
    "ultrices", "duis", "eget", "gravida", "metus",
    "a", "maximus", "nullam", "porttitor", "sem",
    "id", "dictum", "sapien", "quam", "hendrerit",
    "ante", "sit", "amet", "orci", "efficitur",
    "donec", "interdum", "ultricies", "semper",
    "vitae", "purus", "sollicitudin",
    "molestie", "arcu", "vel", "suscipit", "ante",
    "tempus", "id", "nullam", "egestas", "semper",
    "sem", "in", "sodales", "justo", "sodales",
    "et", "nullam", "non", "orci", "in", "sapien",
    "dapibus", "feugiat", "aenean", "porta",
    "mauris", "sit", "amet", "sodales", "urna",
    "faucibus", "scelerisque", "eros", "aliquam",
    "congue", "consequat", "turpis", "sodales",
    "in", "sapien", "non", "vestibulum", "eget",
    "vehicula", "sapien", "aliquam", "eros",
    "pellentesque", "ornare", "donec", "hendrerit",
    "sodales", "donec", "a", "suscipit", "diam",
    "quis", "pellentesque", "sapien", "scelerisque",
    "at", "massa", "ut", "aliquet", "ante", "a",
    "sollicitudin", "risus", "tempus", "euismod",
    "sed", "finibus", "quam", "ac", "aliquam",
    "congue", "turpis", "quam", "hendrerit",
    "purus", "ac", "interdum", "nullam",
    "sagittis", "enim", "non", "congue",
    "nulla", "in", "consectetur", "purus",
    "fermentum", "justo", "maximus",
    "tempus", "nulla", "quis", "vestibulum",
    "nulla", "porta", "ut", "semper",
    "elementum", "lorem", "in", "ornare",
    "metus", "amet", "iaculis", "ex",
    "quam", "est",
    "viverra", "ut", "pellentesque",
    "posuere", "duis", "vitae", "dictum",
    "velit", "elit", "pellentesque", "pharetra",
    "commodo", "erat", "vitae",
    "ultricies", "tincidunt", "nunc", "ornare",
    "non", "velit", "id", "fermentum",
    "nunc", "sed", "tincidunt", "diam",
    "vel", "porttitor", "lectus", "a",
    "metus", "sed", "iaculis",
    "erat", "ut", "fringilla", "magna",
    "quis", "posuere", "nunc", "tincidunt",
    "consequat", "eros", "sodales", "sem",
    "nec", "elementum", "mi", "cras",
    "suscipit", "elit", "tincidunt",
    "eleifend", "velit", "eu",
    "ultricies", "auctor", "justo", "suscipit",
    "consectetur", "adipiscing", "elit", "sed",
    "tempor", "incididunt",
    "labore", "magna",
    "aliqua", "nostrud", "exercitation",
    "ullamco", "laboris", "nisi",
    "irure", "in", "reprehenderit",
    "esse", "cillum", "dolore", "eu",
    "fugiat", "pariatur", "excepteur", "sint",
    "cupidatat", "non",
    "proident", "sunt", "culpa", "qui",
    "deserunt", "mollit", "anim", "id",
    "perspiciatis", "unde", "omnis", "iste", "natus", "error",
    "voluptatem", "accusantium", "doloremque",
    "laudantium", "totam", "rem", "aperiam",
    "eaque", "ipsa", "quae", "ab", "illo",
    "inventore", "veritatis", "et", "quasi",
    "architecto", "beatae", "vitae", "dicta",
    "explicabo", "nemo", "enim", "ipsam",
    "voluptatem", "quia", "voluptas", "sit",
    "aspernatur", "aut", "odit", "aut", "fugit",
    "consequuntur", "magni", "dolores", "eos",
    "ratione", "sequi", "nesciunt", "neque",
    "porro", "quisquam", "est", "qui", "dolorem",
    "quia", "dolor", "amet",
    "adipisci", "velit", "sed",
    "quia", "numquam", "eius", "modi",
    "tempora", "incidunt", "magnam", "aliquam", "quaerat",
    "enim", "minima",
    "nostrum", "exercitationem",
    "ullam", "corporis", "suscipit", "laboriosam",
    "aliquid", "commodi",
    "consequatur", "autem", "vel", "eum", "iure",
    "reprehenderit", "qui", "ea", "veniam",
    "laboriosam",
]

_word_pool = LOREM_WORDS * 10
_rng.shuffle(_word_pool)


def get_lorem_word():
    return _rng.choice(_word_pool)


def generate_lorem(min_words, max_words):
    n = _rng.randint(min_words, max_words)
    words = [get_lorem_word() for _ in range(n)]
    text = ' '.join(words)
    return text[0].upper() + text[1:] + '.'


# Tag-specific word counts
TAG_MIN_WORDS = {
    'title': 4, 'h1': 6, 'h2': 5, 'h3': 4, 'h4': 4,
    'h5': 3, 'h6': 3,
    'a': 2, 'button': 2, 'li': 5, 'option': 2, 'span': 2,
    'label': 2, 'p': 20, 'blockquote': 15,
    'figcaption': 5, 'dd': 10, 'td': 8, 'th': 4, 'legend': 3,
    'dt': 3, 'summary': 5,
}
TAG_MAX_WORDS = {
    'title': 10, 'h1': 12, 'h2': 10, 'h3': 8, 'h4': 7,
    'h5': 8, 'h6': 8,
    'a': 6, 'button': 5, 'li': 15, 'option': 4, 'span': 8,
    'label': 5, 'p': 50, 'blockquote': 40,
    'figcaption': 15, 'dd': 30, 'td': 20, 'th': 12, 'legend': 8,
    'dt': 8, 'summary': 15,
}
DEFAULT_MIN = 3
DEFAULT_MAX = 15

SKIP_TAG_NAMES = {'script', 'style', 'code', 'pre', 'noscript', 'template', 'textarea'}

# Patterns to skip (URLs, paths, numbers-only, etc.)
SKIP_TEXT_PATTERNS = [
    re.compile(r'^[\d\s\.\,\/\\\:\;\(\)\[\]\{\}\"\'\`\|\+\=\-\*\!\@\#\$\%\^\&\<\>]+$'),
    re.compile(r'^https?://'),
    re.compile(r'^www\.'),
    re.compile(r'^assets/'),
    re.compile(r'^\.\./'),
    re.compile(r'^#[a-zA-Z][\w:.-]*$'),
    re.compile(r'^[a-zA-Z_][\w-]*(?:\.[a-zA-Z_][\w-]*)*$'),
    re.compile(r'^\s*[\r\n]+\s*$'),
]


def should_skip_text(text):
    stripped = text.strip()
    if not stripped:
        return True
    for pat in SKIP_TEXT_PATTERNS:
        if pat.match(stripped):
            return True
    if stripped.startswith('{') or stripped.startswith('['):
        return True
    # Skip social media handles/URLs
    if re.match(r'^(@|#)[\w]+$', stripped):
        return True
    return False


def get_tag_name_at_pos(pos, content):
    before = content[:pos]
    last_lt = before.rfind('<')
    if last_lt == -1:
        return None
    tag_section = before[last_lt:]
    tag_match = re.match(r'</?([a-zA-Z][^\s/>]*)', tag_section)
    if tag_match:
        return tag_match.group(1)
    return None


def get_skip_regions(content):
    """Get regions to skip (script, style, etc.)."""
    skip_regions = []
    for tag_name in SKIP_TAG_NAMES:
        pattern = re.compile(
            rf'<{tag_name}[^>]*>.*?</{tag_name}>',
            re.DOTALL | re.IGNORECASE
        )
        for m in pattern.finditer(content):
            skip_regions.append((m.start(), m.end()))
    return skip_regions


def is_inside_skip(pos, skip_regions):
    for start, end in skip_regions:
        if start <= pos <= end:
            return True
    return False


def replace_meta_content(content):
    """Replace content in meta tags (description, keywords, og:title, etc.)."""
    # Match meta tags with content attributes that contain text
    meta_pattern = re.compile(
        r'<meta[^>]*content="([^"]{10,200})"[^>]*>',
        re.IGNORECASE
    )
    replacements = []

    for m in meta_pattern.finditer(content):
        orig = m.group(1)
        # Skip if it's a URL or path
        if orig.startswith('http') or orig.startswith('assets/') or orig.startswith('//'):
            continue
        # Generate replacement text
        n = _rng.randint(15, 50)
        words = [_rng.choice(_word_pool) for _ in range(n)]
        replacement = ' '.join(words)
        replacement = replacement[0].upper() + replacement[1:] + '.'
        replacements.append((m.start(1), m.end(1), replacement))

    # Apply replacements in reverse order
    for start, end, text in reversed(replacements):
        content = content[:start] + text + content[end:]

    return content


def replace_jsonld_content(content):
    """Replace text values in JSON-LD script tags."""
    # Find JSON-LD blocks
    jsonld_pattern = re.compile(
        r'(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',
        re.DOTALL | re.IGNORECASE
    )

    def replace_json_values(match):
        prefix = match.group(1)
        json_text = match.group(2)
        suffix = match.group(3)

        # Replace string values in JSON (not URLs, not numeric)
        # Match "field": "some text" patterns
        def replace_string(m):
            key = m.group(1)
            value = m.group(2)
            # Skip URLs, paths, short values
            if value.startswith('http') or value.startswith('//') or value.startswith('/'):
                return m.group(0)
            if value.startswith('assets/') or value.startswith('www.'):
                return m.group(0)
            # Skip phone numbers, emails, zip codes
            if re.match(r'^[\d\+\-\(\)\s]+$', value):
                return m.group(0)
            # Skip very short values (names, types, etc.)
            if len(value) < 5:
                return m.group(0)
            # Generate lorem replacement
            n = min(len(value.split()) * 2, 30)
            n = max(n, 5)
            words = [_rng.choice(_word_pool) for _ in range(n)]
            replacement = ' '.join(words)
            replacement = replacement[0].upper() + replacement[1:] + '.'
            return f'"{key}": "{replacement}"'

        json_text = re.sub(r'"([^"]+)":\s*"([^"]+)"', replace_string, json_text)
        return prefix + json_text + suffix

    content = jsonld_pattern.sub(replace_json_values, content)
    return content


def replace_text(content):
    """Replace text between HTML tags with Lorem Ipsum."""
    skip_regions = get_skip_regions(content)

    # Also skip JSON-LD (we handle it separately)
    jsonld_pattern = re.compile(
        r'<script[^>]*type="application/ld\+json"[^>]*>.*?</script>',
        re.DOTALL | re.IGNORECASE
    )
    for m in jsonld_pattern.finditer(content):
        skip_regions.append((m.start(), m.end()))

    # Collect all replacements first (position-based)
    replacements = []

    # Find all text nodes between > and <
    for m in re.finditer(r'>([^<]{2,10000})<', content):
        text_start = m.start() + 1
        text_end = m.end() - 1
        text = m.group(1)

        # Skip if inside a skip region
        if is_inside_skip(text_start, skip_regions):
            continue

        # Skip if text should not be replaced
        if should_skip_text(text):
            continue

        # Get tag name for word count
        tag_name = get_tag_name_at_pos(text_start, content)
        if tag_name is None:
            continue

        min_w = TAG_MIN_WORDS.get(tag_name, DEFAULT_MIN)
        max_w = TAG_MAX_WORDS.get(tag_name, DEFAULT_MAX)

        # If text is very long (like a paragraph), use more words
        actual_words = len(text.strip().split())
        if actual_words > 30:
            min_w = max(min_w, actual_words)
            max_w = max(max_w, actual_words * 2)

        replacement = generate_lorem(min_w, max_w)
        replacements.append((text_start, text_end, replacement))

    # Apply replacements in reverse order to maintain positions
    replacements.sort(key=lambda x: x[0], reverse=True)
    for start, end, text in replacements:
        content = content[:start] + text + content[end:]

    return content


def process_file(filepath):
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  SKIP (read error): {filepath.name} — {e}")
        return False

    if filepath.suffix != '.html':
        return False

    # Step 1: Replace regular HTML text
    new_content = replace_text(content)

    # Step 2: Replace meta content attributes
    new_content = replace_meta_content(new_content)

    # Step 3: Replace JSON-LD content
    new_content = replace_jsonld_content(new_content)

    if new_content != content:
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
                print(f"  {filepath.relative_to(BASE)} — text replaced")

    print(f"\nDone! Replaced text content on {total} pages.")


if __name__ == "__main__":
    main()
