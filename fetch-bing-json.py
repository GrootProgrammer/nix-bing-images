import json
import hashlib
import requests  # pyright: ignore[reportMissingModuleSource]
from typing import List, Dict
import urllib.request

def map_entries_with_image_hash(entries: List[Dict], urlhash: Dict) -> List[Dict]:
    """
    Maps over JSON entries and returns a new list of dicts with:
      - title: previous title
      - url: previous url
      - hash: SHA-256 hash of the fetched image
    """
    result = []

    for i, entry in enumerate(entries):
        image_url = entry["url"]
        if image_url in urlhash:
            image_hash = urlhash[image_url]
        else:
            response = requests.get(image_url)
            response.raise_for_status()

            image_bytes = response.content
            image_hash = hashlib.sha256(image_bytes).hexdigest()
            print(float(i*100) / len(entries))

        if entry["title"] is None or entry["title"] == "null":
            continue
        if entry["date"] is None or entry["date"] == "null":
            continue
        if entry["url"] is None or entry["url"] == "null":
            continue

        result.append({
            "title": entry["title"],
            "date": entry["date"],
            "url": image_url,
            "hash": image_hash,
        })

    return result

with urllib.request.urlopen("https://raw.githubusercontent.com/npanuhin/Bing-Wallpaper-Archive/refs/heads/master/api/ROW/en.json") as response:
    entries = json.load(response)
with open("wallpapers-with-hash.json", 'r') as f:
    cached = json.load(f)
    dcache = {}
    for i in cached:
        dcache[i["url"]] = i["hash"]

mapped = map_entries_with_image_hash(entries,dcache)

with open("wallpapers-with-hash.json", "w") as f:
    json.dump(mapped, f, indent=2)

