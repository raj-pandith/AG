import re

with open('c:/My Web Sites/Jain2/mainfolder.com/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

count = 0

def swap_attributes(match):
    global count
    full = match.group(0)
    # Parse the <a> tag to swap href and data-original-href values
    parts = re.match(
        r'(<a\s+[^>]*?)(href\s*=\s*["\'])([^"\']*?)(["\'])([^>]*?)(data-original-href\s*=\s*["\'])([^"\']*?)(["\'])([^>]*>)',
        full,
        re.IGNORECASE | re.DOTALL
    )
    if parts:
        pre = parts.group(1)         # <a ... before href
        href_attr = parts.group(2)   # href=
        href_val = parts.group(3)    # current href value
        close1 = parts.group(4)      # closing quote
        middle = parts.group(5)      # stuff between href and data-original-href
        doh_attr = parts.group(6)    # data-original-href=
        doh_val = parts.group(7)     # current data-original-href value
        close2 = parts.group(8)      # closing quote
        post = parts.group(9)        # remaining attrs and >
        count += 1
        # Swap: href gets the original link, data-original-href gets the CommingSoon URL
        return f'{pre}{href_attr}{doh_val}{close1}{middle}{doh_attr}{href_val}{close2}{post}'
    return full

# Match <a> tags that contain BOTH href and data-original-href
content = re.sub(
    r'<a\s+[^>]*?href\s*=\s*["\'][^"\']*?["\'][^>]*?data-original-href\s*=\s*["\'][^"\']*?["\'][^>]*?>',
    swap_attributes,
    content,
    flags=re.DOTALL | re.IGNORECASE
)

with open('c:/My Web Sites/Jain2/mainfolder.com/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Swapped attributes in {count} <a> tags')
