from typing import List
from datetime import datetime
from email.utils import parsedate_to_datetime


def filter_entries_by_published_today(entries):
    today = datetime.utcnow().date()
    result = []

    for entry in entries:
        if "published_parsed" in entry:
            entry_date = datetime(*entry["published_parsed"][:6]).date()
        elif "updated_parsed" in entry:
            entry_date = datetime(*entry["updated_parsed"][:6]).date()
        else:
            pub_date = entry.get("published") or entry.get("updated")

            if not pub_date:
                continue
            try:
                entry_date = parsedate_to_datetime(pub_date).date()
            except Exception:
                continue
            
        if entry_date == today:
            result.append()
    return result

def filter_entries_by_keywords(entries: list, keywords: List[str]) -> list:
    """Return entries that match any of the given keywords in the title or summary."""
    if not keywords:
        return entries  # No filtering needed

    filtered = []
    for entry in entries:
        title = entry.get("title", "").lower()
        summary = entry.get("summary", "").lower()

        if any(keyword.lower() in title or keyword.lower() in summary for keyword in keywords):
            filtered.append(entry)

    return filtered

def get_entry_id(entry: dict) -> str:
    """
    Get a stable ID for an entry. Tries:
    - entry.id (most reliable)
    - entry.link
    - fallback: hash of title + published
    """
    if "id" in entry:
        return entry["id"]
    elif "link" in entry:
        return entry["link"]
    else:
        # fallback to deterministic string
        return f"{entry.get('title', '')}-{entry.get('published', '')}"
