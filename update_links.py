import re

with open('c:/My Web Sites/Jain2/mainfolder.com/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_href = './mainfolder.com/ojix-work/CommingSoon.html'

# Match: <li ... > <a ... href="ORIGINAL" ... >TEXT</a> </li>
# Group 1: <li ...><a ... (everything up to href=)
# Group 2: ORIGINAL href value
# Group 3: closing quote and rest of <a> tag
# Group 4: link text + </a></li>
pattern = r'(<li[^>]*>\s*<a\s+[^>]*?href\s*=\s*["\'])([^"\']+?)(["\'][^>]*>.*?</a>\s*</li>)'

count = 0

def replacer(match):
    global count
    prefix = match.group(1)      # <li...><a...href=
    original = match.group(2)    # original href value
    suffix = match.group(3)      # rest of tag

    # Skip external links, anchors, and PDFs
    if original.startswith('http') or original.startswith('#') or original.lower().endswith('.pdf'):
        return match.group(0)

    count += 1
    # Replace href with new value and add data-original-href
    return f'{prefix}{new_href}{suffix[:-5]} data-original-href="{original}">{suffix[-5:]}'

new_content = re.sub(pattern, replacer, content, flags=re.DOTALL | re.IGNORECASE)

if new_content != content:
    with open('c:/My Web Sites/Jain2/mainfolder.com/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'SUCCESS: Modified {count} <a> tags in <li> elements')
else:
    print('WARNING: No changes made')
