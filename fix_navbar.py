#!/usr/bin/env python3
"""
Insert the Animate Content marquee section into all non-home HTML pages
so the navbar layout matches the home page exactly.
"""

import os
import re
from pathlib import Path

BASE = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com")
EXCLUDE_DIRS = {"admissions-2026-27"}

# The exact block from index.html to insert before <div class="sticky-wrapper">
# on every non-home page. Includes the marquee + inline style for .logo-bg.
ANIMATE_CONTENT_BLOCK = '''        <!-- Animate Content Start -->
        <div class="animate__content sp_bottom_15 sp_top_15">
            <div class="container-fluid full__width__padding">
                <div class="animate__content__marquee">
                    <div class="animate__content__track">
                        <div class="animate__content__item"><span class="cbse-affil-badge"><i class="fa-solid fa-certificate"></i> CBSE Affiliation No: 831454</span></div>
                        <div class="animate__content__item"><a href="#" style="color:#001c54;">Finnish Education</a>
                        </div>
                        <div class="animate__content__item"><a href="#" style="color:#ffa500;">Best School</a></div>
                        <div class="animate__content__item"><a href="#" style="color:#001c54;">Preschool–Grade 10</a>
                        </div>
                        <div class="animate__content__item"><a href="#" style="color:#ffa500;">Admissions Open</a></div>
                        <div class="animate__content__item"><span>2026–2027</span></div>
                        <div class="animate__content__item" style="color:#ffa500;">Limited Seats</div>
                        <div class="animate__content__item"><span>Book Your Admission</span></div>
                        <div class="animate__content__item" style="color:#ffa500;">Register Now</div>

                        <!-- Duplicate for seamless loop -->
                        <div class="animate__content__item"><span class="cbse-affil-badge"><i class="fa-solid fa-certificate"></i> CBSE Affiliation No: 831454</span></div>
                        <div class="animate__content__item"><a href="#" style="color:#001c54;">Finnish Education</a>
                        </div>
                        <div class="animate__content__item"><a href="#" style="color:#ffa500;">Best School</a></div>
                        <div class="animate__content__item"><a href="#" style="color:#001c54;">Preschool–Grade 10</a>
                        </div>
                        <div class="animate__content__item"><a href="#" style="color:#ffa500;">Admissions Closing Soon</a></div>
                        <div class="animate__content__item"><span>2026–2027</span></div>
                        <div class="animate__content__item" style="color:#ffa500;">Limited Seats</div>
                        <div class="animate__content__item"><span>Book Your Admission</span></div>
                        <div class="animate__content__item" style="color:#ffa500;">Register Now</div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Animate Content End -->


        <style>
            .logo-bg {
                mask-image: url("assets/img/logo_bg_mask.png");
            }
        </style>

        <!-- animate condtent end-->

'''


def process_file(filepath):
    """Insert the Animate Content block before sticky-wrapper if not already present."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  SKIP (read error): {filepath} — {e}")
        return False

    # Skip index.html (home page already has it)
    if filepath.name in ('index.html', 'index-2.html'):
        return False

    # Skip if already has Animate Content
    if 'Animate Content Start' in content:
        return False

    # Check for sticky-wrapper (required insertion point)
    if '<div class="sticky-wrapper">' not in content:
        return False

    # Insert the block before <div class="sticky-wrapper">
    marker = '<div class="sticky-wrapper">'
    idx = content.index(marker)

    # Make sure we're inside the header (not a duplicate sticky-wrapper)
    # Check that there's a header-top closing </div> nearby before the marker
    header_section = content[:idx]
    if 'header-top' not in header_section or '<header class=' not in header_section:
        return False

    new_content = content[:idx] + ANIMATE_CONTENT_BLOCK + content[idx:]

    if new_content != content:
        filepath.write_text(new_content, encoding='utf-8')
        return True

    return False


def main():
    total = 0
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for fname in files:
            if not fname.endswith('.html'):
                continue
            filepath = Path(root) / fname
            if process_file(filepath):
                total += 1
                print(f"  {filepath.relative_to(BASE)} — navbar updated")

    print(f"\nDone! Updated navbar on {total} pages.")


if __name__ == "__main__":
    main()
