import os

# Base folder (change if needed)
base_folder = os.getcwd()

# Image extensions
image_extensions = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff")

for root, dirs, files in os.walk(base_folder):
    # ❌ Remove "ojixs" from directories to skip it completely
    if "ojixs" in dirs:
        dirs.remove("ojixs")

    for filename in files:
        if filename.lower().endswith(image_extensions):
            old_path = os.path.join(root, filename)

            name, ext = os.path.splitext(filename)
            new_filename = f"{name}-1{ext}"
            new_path = os.path.join(root, new_filename)

            # Prevent overwrite
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} → {new_path}")
            else:
                print(f"Skipped (exists): {new_path}")

print("Done processing images (excluding 'ojixs').")