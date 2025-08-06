## 📰 RSS to Discord Webhook Notifier

This is a lightweight Python tool that monitors RSS feeds and sends **batched updates** to specified Discord webhooks using **embeds**. Designed for self-hosting, the tool supports:

- ✅ Configurable rate limiting and batch sizes  
- ✅ Markdown-friendly formatting  
- ✅ YouTube video thumbnail support  
- ✅ Persistent caching to avoid reposting  
- ✅ Cron-compatible & Docker-friendly  
- ✅ Configurable via `config.yaml`

---

## 🔧 How It Works

1. You define RSS feeds and corresponding Discord webhooks in `config.yaml`.
2. The tool checks each feed and parses the most recent items.
3. Only **new** items (not already sent) are delivered as Discord embeds.
4. Feeds are **batched** (default: 5 items per message).
5. Already-sent items are tracked using a `sent_items.json` cache.

---

## 📦 Configuration

All configuration is stored in a human-readable `config.yaml` file at the project root.

### Example:

```yaml
feeds:
  - name: "Hacker News"
    url: "https://hnrss.org/frontpage"
    webhook: "https://discord.com/api/webhooks/..."

  - name: "YouTube - Fireship"
    url: "https://www.youtube.com/feeds/videos.xml?channel_id=UCsBjURrPoezykLs9EqgamOA"
    webhook: "https://discord.com/api/webhooks/..."

rate_limit_seconds: 5         # Delay between messages to avoid hitting Discord rate limits
batch_size: 5                 # Max number of items sent in a single message
max_items_per_feed: 100       # Max number of sent item IDs to keep per feed
```

---

## 🚀 Usage

This project uses [Poetry](https://python-poetry.org/) for dependency management.

1. **Install Poetry** (if you don't have it yet):

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -

2. **Install dependencies**
  ```bash
    poetry install

3. **Activate the virtual environment (optional but recommended):**
  ```bash
    poetry shell

4. **Run the bot**
  ```bash
    poetry run python main.py
---

## 🐳 Docker

### Dockerfile Included!

You can build and run the tool in Docker:

```bash
docker build -t rss-discord-bot .
```

### Recommended Docker Run

```bash
docker run -d \
  --name rss-discord \
  -v $(pwd)/config.yaml:/app/config.yaml \
  -v $(pwd)/sent_items.json:/app/sent_items.json \
  rss-discord-bot
```

This ensures:
- Your `config.yaml` is **editable** outside the container
- Your `sent_items.json` cache is **persistent**

---

## ⏱ Automating with Cron

You can schedule it to run every few hours using cron (outside or inside Docker):

### Example (Every 6 Hours):

```cron
0 */6 * * * docker exec rss-discord python main.py >> rss-discord.log 2>&1
```

Or outside Docker:

```cron
0 */6 * * * cd /path/to/project && python3 main.py >> rss-discord.log 2>&1
```

---

## 🧠 How Duplication Is Prevented

The tool stores a lightweight JSON file (`sent_items.json`) which tracks the latest sent items **per feed**. To limit file size, it keeps only the most recent `max_items_per_feed` entries per feed (default: 100).

This file is updated safely after each successful run.

---

## 📺 YouTube Thumbnails

When the feed is a YouTube channel, the tool will **extract and embed the video thumbnail** automatically in the Discord embed.

---

## 📁 Project Structure

```
.
├── config.yaml           # Main configuration file
├── sent_items.json       # Local cache of sent items
├── main.py               # Entrypoint
├── feed_handler.py       # Fetches and parses feeds
├── webhook_sender.py     # Sends messages to Discord
├── storage.py            # Load/save cache
├── Dockerfile            # Docker support
└── requirements.txt      # Python dependencies
```

---

## ✅ Features in Use

- `feedparser` – RSS feed parsing
- `requests` – Sending Discord webhooks
- Markdown formatting and HTML-to-Markdown cleaning
- Safe JSON writes
- Supports **multiple feeds and webhooks**
- Configurable in one file

---

## 🔒 Security Considerations

- Your `config.yaml` file contains sensitive Discord webhook URLs.  
  **Do not commit or share this file publicly.**
- To revoke a webhook: Go to Discord → Channel Settings → Integrations → Webhooks.

---

## 🛠 Contributing

Feel free to fork and improve! PRs welcome for:
- Better formatting
- More platform support (e.g. Telegram, Slack)
- Caching improvements (e.g. SQLite)
