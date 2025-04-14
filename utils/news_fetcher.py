# utils/news_fetcher.py
# 📡 암호화폐 관련 뉴스 수집 모듈 (RSS 기반 다기관)

import feedparser
import random

# ✅ 사용할 주요 한글 뉴스 RSS 출처 목록 (암호화폐/경제 중심)
RSS_FEEDS = [
    ("연합뉴스", "https://www.yna.co.kr/rss/economy.xml"),
    ("한겨레", "https://www.hani.co.kr/rss/economy.xml"),
    ("이데일리", "https://www.edaily.co.kr/rss/economy.xml"),
    ("조선비즈", "https://biz.chosun.com/rss/chosen_biz.xml"),
    ("서울경제", "https://www.sedaily.com/rss/NewsList.xml"),
    ("블로터", "https://www.bloter.net/rss")
]

# 🔎 코인 관련 키워드
CRYPTO_KEYWORDS = [
    "비트코인", "이더리움", "암호화폐", "가상자산", "코인", "블록체인", "업비트", "바이낸스", 
    "리플", "XRP", "SEC", "ETF", "금융위", "나스닥", "파월", "연준", "CPI", "금리", "도지", 
    "테더", "테슬라", "트위터", "AI", "중국", "트럼프", "전쟁", "우크라이나", "하락", "급등"
]

def fetch_news(max_articles=6):
    """
    📥 다기관 뉴스 기사 수집 및 필터링
    - 코인 관련 키워드 포함 기사만 추출
    - 기관당 하나씩 섞어서 최대 max_articles 반환
    - 감정분석용으로 텍스트 포함, 기본 감정 점수는 0.0
    """
    all_news = []

    for name, url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")
            content = title + " " + summary

            if any(keyword in content for keyword in CRYPTO_KEYWORDS):
                news_item = {
                    "title": title,
                    "summary": summary,
                    "url": link,
                    "source": name,
                    "sentiment": 0.0  # 초기값, 이후 분석 모듈에서 대체
                }
                all_news.append(news_item)
                break  # 기관당 1개만 사용

    # 무작위로 순서 섞기 + 상한 제한
    random.shuffle(all_news)
    return all_news[:max_articles]
