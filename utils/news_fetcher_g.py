# utils/news_fetcher_g.py
import feedparser

def fetch_news():
    try:
        feed = feedparser.parse("https://news.google.com/rss/search?q=cryptocurrency&hl=en-US&gl=US&ceid=US:en")
        news_items = []
        for entry in feed.entries[:10]:
            news_items.append({
                "title": entry.title,
                "url": entry.link,
                "source": entry.source.title if hasattr(entry.source, "title") else "Unknown",
                "published": entry.published
            })
        print(f"뉴스 데이터 수집 성공: {len(news_items)}개")
        return news_items
    except Exception as e:
        print(f"뉴스 수집 실패: {e}")
        return []