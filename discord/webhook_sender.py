import requests
import time
from datetime import datetime
from email.utils import parsedate_to_datetime
import urllib.parse
import html2text

h = html2text.HTML2Text()
h.ignore_links = False  # Keep links as Markdown links
h.ignore_images = True  # Skip images (thumbnails handled separately)
h.body_width = 0        # Disable automatic wrapping

def send_discord_batch(entries: list, webhook_url: str, feed_name: str):
    """Send a batch of RSS entries as Discord embeds, with YouTube thumbnails if applicable."""
    embeds = []

    for entry in entries[:5]:  # Limit to 5 most recent
        title = entry.get("title", "No title")
        url = entry.get("link", "")
        description_html = entry.get("summary", "")
        description = h.handle(description_html).strip()[:2048]
        timestamp = entry.get("published", None)

        if timestamp:
            try:
                timestamp = parsedate_to_datetime(timestamp).isoformat()
            except Exception:
                timestamp = None

        embed = {
            "title": title,
            "url": url,
            "description": description,
            "footer": {"text": feed_name},
        }

        if timestamp:
            embed["timestamp"] = timestamp

        # Try to get YouTube video ID and add thumbnail
        video_id = entry.get("yt_videoid")
        if not video_id and "youtube.com/watch?v=" in url:
            # fallback: extract video id from URL param
            query = urllib.parse.urlparse(url).query
            params = urllib.parse.parse_qs(query)
            video_id = params.get("v", [None])[0]

        if video_id:
            embed["thumbnail"] = {
                "url": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            }

        embeds.append(embed)

    if not embeds:
        return

    payload = {
        "embeds": embeds
    }

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 429:
            retry_after = response.json().get("retry_after", 1000) / 1000
            print(f"⚠️ Rate limited. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
            return send_discord_batch(entries, webhook_url, feed_name)
        response.raise_for_status()
        print(f"✅ Sent batch of {len(embeds)} entries to {feed_name}")
    except requests.RequestException as e:
        print(f"❌ Failed to send Discord batch: {e}")
