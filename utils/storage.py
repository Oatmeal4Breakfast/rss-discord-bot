import os
import json

MAX_ITEMS_PER_FEED = 100  # You could even make this configurable later

def prune_sent_items(sent_items: dict) -> dict:
    """Prune the sent_items dictionary to keep only the most recent N entries per feed."""
    for feed_url in sent_items:
        sent_items[feed_url] = sent_items[feed_url][-MAX_ITEMS_PER_FEED:]
    return sent_items


def load_sent_items(cache_path: str) -> dict:
    """Load the sent items cache from a JSON file."""
    if not os.path.exists(cache_path):
        return {}

    with open(cache_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("⚠️  Failed to decode sent_items.json. Starting fresh.")
            return {}

def save_sent_items(cache_path: str, data: dict) -> None:
    """Save the sent items cache to a JSON file."""
    pruned = prune_sent_items(data)
    with open(cache_path, "w") as f:
        json.dump(pruned, f, indent=2)
