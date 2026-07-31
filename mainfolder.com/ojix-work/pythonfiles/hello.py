from bs4 import BeautifulSoup

INPUT_FILE = "mainfolder.com\index.html"
OUTPUT_FILE = "index_updated.html"

REPLACEMENT_LINK = "mainfolder.com\ojix-work\CommingSoon.html"

def process_html():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]

        if href.endswith(".html"):
            # store original link
            a_tag["data-original-href"] = href
            
            # replace href
            a_tag["href"] = REPLACEMENT_LINK

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print("Updated file saved as:", OUTPUT_FILE)

if __name__ == "__main__":
    process_html()