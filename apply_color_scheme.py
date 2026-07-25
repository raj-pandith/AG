#!/usr/bin/env python3
"""Replace colors in style.css to implement artisan patisserie theme."""

from pathlib import Path

STYLE_CSS = Path(r"c:\My Web Sites\Jain2\jainheritageschool.com\assets\css\style.css")

with open(STYLE_CSS, encoding='utf-8') as f:
    content = f.read()

# Color replacement mapping: (old, new, description)
REPLACEMENTS = [
    # Variables section - CSS custom properties
    ('--theme-color: #1a2653;', '--theme-color: #7c381a;'),
    ('--primary-color: #1a2653;', '--primary-color: #7c381a;'),
    ('--title-color: #001c54;', '--title-color: #7c381a;'),
    ('--yellow-color: #FFB539;', '--yellow-color: #f3bb1d;'),
    ('--brand-color: #79F4E4;', '--brand-color: #f9e277;'),
    ('--smoke-color: #F2F5FA;', '--smoke-color: #fffef4;'),
    ('--light-blue-color: #001C49;', '--light-blue-color: #fffef4;'),

    # Direct color replacements in CSS rules
    ('#1a2653', '#7c381a'),  # Dark blue → Chocolate
    ('#001c54', '#7c381a'),  # Darker blue → Chocolate
    ('#001C49', '#7c381a'),  # Dark blue variant → Chocolate
    ('#0b1422', '#7c381a'),  # Very dark blue → Chocolate
    ('#113D48', '#7c381a'),  # Teal-dark → Chocolate

    # Golden/yellow accents
    ('#F8BC22', '#f3bb1d'),  # Golden → Vibrant golden
    ('#FFB539', '#f3bb1d'),  # Orange-yellow → Vibrant golden
    ('#FFA944', '#f3bb1d'),  # Orange → Vibrant golden
    ('#ffa500', '#f3bb1d'),  # Pure orange → Vibrant golden

    # Background/surface colors
    ('#F2F5FA', '#fffef4'),  # Light gray-blue → Warm cream
    ('#E9F6F9', '#fdf8d8'),  # Light blue → Pale butter cream
    ('#F3F4F6', '#fdf8d8'),  # Light gray → Pale butter cream

    # Gray colors → butter cream tones
    ('#E1E4E5', '#fdf8d8'),  # Gray → Pale butter cream
    ('#E1E4E6', '#fdf8d8'),  # Gray variant → Pale butter cream
    ('#B1B8C3', '#f9e277'),  # Gray-blue → Soft butter yellow
]

total_replacements = 0
for old, new in REPLACEMENTS:
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        total_replacements += count
        print('Replaced ' + old + ' -> ' + new + ' (' + str(count) + ' occurrences)')

with open(STYLE_CSS, 'w', encoding='utf-8') as f:
    f.write(content)

print()
print(f'Total replacements made: {total_replacements}')
print('style.css updated successfully!')
