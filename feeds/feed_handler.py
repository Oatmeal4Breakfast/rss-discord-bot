import feedparser

def fetch_feed_entries(feed_url: str, max_items=5) -> list:
    """Fetch and parse RSS feed entries from the given URL."""
    feed = feedparser.parse(feed_url)
    entries = []
    for entry in feed.entries[:max_items]:
        entries.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary if 'summary' in entry else '',
        })
    if feed.bozo:
        print(f"⚠️  Failed to parse feed: {feed_url}")
        return []

    return feed.entries