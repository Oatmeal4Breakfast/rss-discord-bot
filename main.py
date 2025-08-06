import yaml
import os
from feeds.feed_handler import fetch_feed_entries
from utils.filters import filter_entries_by_keywords, get_entry_id, filter_entries_by_published_today
from discord.webhook_sender import send_discord_batch
from utils.storage import load_sent_items, save_sent_items, prune_sent_items

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")
CACHE_PATH = os.path.join(BASE_DIR, "sent_items.json")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    sent_items = load_sent_items(CACHE_PATH)

    rate_limit_delay = config.get("rate_limit_delay", 0.5)
    batch_size = config.get("batch_size", 5)

    for feed in config.get("feeds", []):
        feed_name = feed["name"]
        feed_url = feed["url"]
        webhook_url = feed.get("webhook") or config.get("default_webhook")
        keywords = feed.get("keywords", [])

        print(f"🔍 Checking feed: {feed_name}")
        entries = fetch_feed_entries(feed_url)

        # Filter by keyword
        filtered_entries = filter_entries_by_keywords(entries, keywords)
        if config.get("filter_by_today", False):
            filtered_entries = filter_entries_by_published_today(filtered_entries)
            
        # Filter out already sent entries
        new_entries = [
            entry for entry in filtered_entries
            if get_entry_id(entry) not in sent_items.get(feed_name, [])
        ]

        # Send newest 5 entries as embed batch
        if new_entries:
            send_discord_batch(new_entries[:batch_size], webhook_url, feed_name)
            for entry in new_entries[:batch_size]:
                sent_items.setdefault(feed_name, []).append(get_entry_id(entry))

        import time
        time.sleep(rate_limit_delay)  # To avoid hitting rate limits
    sent_items = prune_sent_items(sent_items)
    save_sent_items(CACHE_PATH, sent_items)

if __name__ == "__main__":
    main()
