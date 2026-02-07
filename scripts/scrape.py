from collections import defaultdict
import json
import re
import requests

def scrape_audio_data(birds: dict[str, dict], groups: list[str]) -> dict[str, dict]:
    AUDIO_REGEX = re.compile(
        r'''
        jp_container_audio_(?P<audio_index>\d+)
        [\s\S]*?
        (?P<audio_type>
            Calls?|Song|Drum|Display|Juvenile\s+Calls?|Alarm\s+Calls?|Flight\s+Calls?|Flock\s+calls?
        )
        [\s\S]*?
        <span>\s*
            (?P<location_timestamp>[^<]+?)
        \s*</span>
        \s*<a\s+href="(?P<link>https://macaulaylibrary\.org/audio/\d+)"
        ''',
        re.VERBOSE | re.IGNORECASE
    )
    
    # To simulate being a real user
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    results = defaultdict(dict)
    for group, birds in BIRDS.items():
        print(f"Group: {group}")
        for url_name, mnemonic in birds.items():
            url = f"https://www.allaboutbirds.org/guide/{url_name}/sounds"
            print(f"Scraping {url}")
            response = requests.get(url, timeout=15, headers=headers)
            response.raise_for_status()
            html = response.text

            matches = []
            for m in AUDIO_REGEX.finditer(html):
                matches.append({
                    "audio_index": int(m.group("audio_index")),
                    "audio_type": m.group("audio_type").strip(),
                    "location_timestamp": m.group("location_timestamp").strip(),
                    "link": m.group("link") + ".mp3",
                })

            results[group][url_name] = {
                "display_name": url_name.replace("_", " "),
                "mnemonic": mnemonic,
                "url": url,
                "audios": matches
            }

    return results


BIRDS = {
    "group_1": {
        "Great_Blue_Heron": "rok rok rok",
        "Canada_Goose": "honk honk honk",
        "Mallard": "quack quack quack",
        "Hairy_Woodpecker": "squeaky, high-pitched, rapid peek calls, no clearpattern (doesn't go down)",
        "Downy_Woodpecker": "peek peek peek, trill that goes down in pitch",
        "American_Crow": "caw! caw!",
        "Blue_Jay": "jeer, toolool",
        "Gray_Catbird": "meow, chatty talking to itself",
        "Northern_Mockingbird": "many phrases repeated 3-4 times",
        "Cedar_Waxwing": "bzeee bzeee, like a whistle",
        "Dark-eyed_Junco": "musical trill, spaceship",
        "Eastern_Bluebird": "cheer, cheer, cheerful charmer, tur-a-lee",
        "American_Robin": "cheer up, cheerily, cheerio",
        "Wood_Thrush": "eeeee o layyyyyyy tingtingting",
        "Tufted_Titmouse": "peter peter peter, many varied vocalizations",
        "Black-capped_Chickadee": "hey sweetie, chick-a-dee-dee-dee",
        "Red-eyed_Vireo": "Where are you? Here I am!",
        "Turkey_Vulture": "hiss",
        "Red-tailed_Hawk": "keee-aaar",
        "Coopers_Hawk": "nasally cak cak cak",
    },
    "group_2": {} # TODO: add birds here as needed
}

if __name__ == "__main__":
    data = scrape_audio_data(BIRDS, groups=["group_1"])
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)