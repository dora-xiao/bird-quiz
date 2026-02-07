import os
import json

folders = ["group_1", "group_2"]

for folder in folders:
    images_path = os.path.join(folder, "images")
    
    # Check if images folder exists
    if not os.path.exists(images_path):
        print(f"Warning: '{images_path}' does not exist. Skipping.")
        continue
    
    # List all .jpg files and remove the extension
    jpg_files = [
        os.path.splitext(f)[0]
        for f in os.listdir(images_path)
        if f.lower().endswith(".jpg") and os.path.isfile(os.path.join(images_path, f))
    ]
    
    # Write JSON to the folder
    json_path = os.path.join(folder, "image_data.json")
    with open(json_path, "w") as json_file:
        json.dump(sorted(jpg_files), json_file, indent=4)
    
    print(f"Saved image data for '{folder}' to '{json_path}'")
