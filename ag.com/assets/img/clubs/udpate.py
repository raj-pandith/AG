import os
from bs4 import BeautifulSoup

# Folder to scan (change if needed)
base_folder = os.getcwd()

# File extensions to process
web_extensions = (".html", ".htm")

# Walk through all files
for root, dirs, files in os.walk(base_folder):
    for file in files:
        if file.lower().endswith(web_extensions):
            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            soup = BeautifulSoup(content, "html.parser")

            # Find all matching <a> tags
            tags = soup.find_all(
                "a",
                {
                    "target": "_blank",
                    "class": "virtual-tour-btn-animated"
                }
            )

            if tags:
                for tag in tags:
                    tag.decompose()  # remove tag

                # Save updated file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(soup))

                print(f"Updated: {file_path}")

print("Processing completed.")