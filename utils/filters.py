from typing import List

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
