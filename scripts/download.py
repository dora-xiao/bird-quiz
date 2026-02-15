from collections import defaultdict
import json
import os
import requests

data_path = "data.json"
audio_types = ["call", "song"]
locations = [
    "Massachusetts",
    "Rhode Island",
    "Connecticut",
    "New Hampshire",
    "Vermont",
    "New York",
    "Maine",
    "New Jersey",
    "Pennsylvania",
    "Delaware",
    "Maryland",
    "Virginia",
    "West Virginia",
    "Ohio",
    "North Carolina",
]

############################################################
# Choose files

with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for group, group_data in data.items():
    for url_name, bird_data in group_data.items():
        for bird in bird_data["audios"]:
            # Limit to select types of audios
            if not any(a.lower() in bird["audio_type"].lower() for a in audio_types):
                bird["selected"] = False
            # Limit to select locations
            elif not any(l.lower() in bird["location_timestamp"].lower() for l in locations):
                bird["selected"] = False
            else:
                bird["selected"] = True

        # Second pass: fallback if not enough audios
        selected_count = sum(1 for a in bird_data["audios"] if a["selected"])
        if selected_count < 3:
            for bird in bird_data["audios"]:
                bird["selected"] = True

    with open(f"{group}/audio_data.json", "w") as f:
        json.dump(data[group], f, indent=4)

############################################################
# Download files

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

for group, birds in data.items():
    for url_name, bird_data in birds.items():
        for audio in bird_data["audios"]:
            # if not audio["selected"]:
            #     continue

            audio_index = audio["audio_index"]
            base_url = audio["link"]
            mp3_url = base_url

            filename = f"{url_name}_{audio_index}.mp3"
            filepath = os.path.join(f"{group}/audios", filename)

            if os.path.exists(filepath):
                print(f"Skipping existing: {filename}")
                continue

            try:
                print(f"Downloading: {filename}")
                response = session.get(mp3_url, timeout=30, headers=headers)
                response.raise_for_status()

                with open(filepath, "wb") as out:
                    out.write(response.content)

            except Exception as e:
                print(f"Failed {filename}: {e}")

print("Download complete!")
