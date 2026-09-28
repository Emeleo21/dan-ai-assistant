import feedparser

def get_news(topic: str = None) -> str:
    """Get recent news headlines. Pass a topic (e.g. 'technology', 'Nigeria', 'bitcoin') 
    to search that topic, or leave it empty for general top headlines."""
    try:
        if topic:
            url = f"https://news.google.com/rss/search?q={topic}&hl=en-US&gl=US&ceid=US:en"
        else:
            url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"

        feed = feedparser.parse(url)

        if not feed.entries:
            return f"Couldn't find news for {topic or 'top headlines'}"

        headlines = []
        for entry in feed.entries[:5]:
            headlines.append(f"- {entry.title}")

        label = f"Top news on {topic}" if topic else "Top headlines right now"
        return f"{label}:\n" + "\n".join(headlines)
    except Exception as e:
        return f"Error fetching news: {e}"

if __name__ == "__main__":
    print(get_news())
    print()
    print(get_news("Nigeria"))