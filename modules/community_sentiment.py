# 📁 파일명: modules/community_sentiment_finbert.py
# 🎯 목적: Reddit 기반 감정 분석에 금융 특화 모델 FinBERT 적용

import os
import praw
import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# ✅ .env 또는 환경변수에서 Reddit 인증 정보 로드
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "finbert-sentiment-bot")

# ✅ Reddit API 객체 초기화
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# ✅ FinBERT 모델 로드
model_name = "yiyanghkust/finbert-tone"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def analyze_community_sentiment(keyword: str = "bitcoin") -> float:
    """
    Reddit에서 주어진 키워드에 대해 최근 게시글 감정 분석 후 평균 점수 반환
    긍정: +1.0 / 중립: 0 / 부정: -1.0
    """
    try:
        posts = reddit.subreddit("CryptoCurrency").search(keyword, limit=10)
        scores = []
        for post in posts:
            text = post.title + ". " + (post.selftext or "")
            result = sentiment_pipeline(text[:512])[0]
            label = result["label"]
            if label == "positive":
                scores.append(1.0)
            elif label == "neutral":
                scores.append(0.0)
            else:
                scores.append(-1.0)
        if not scores:
            return 0.0
        return round(sum(scores) / len(scores), 2)
    except Exception as e:
        print(f"⚠️ 커뮤니티 감정 분석 실패: {e}")
        return 0.0

def analyze_finbert_sentiment(query="btc OR bitcoin OR crypto", subreddit="CryptoCurrency", limit=20):
    """
    📌 FinBERT 기반 커뮤니티 감정 분석
    :param query: 검색 키워드
    :param subreddit: 분석 대상 서브레딧
    :param limit: 최대 게시물 수
    :return: 감정 점수 (긍정=1, 중립=0, 부정=-1의 평균)
    """
    try:
        posts = reddit.subreddit(subreddit).search(query, sort="new", limit=limit)
        texts = []
        for post in posts:
            if post.title:
                texts.append(post.title)
            if post.selftext:
                texts.append(post.selftext)

        if not texts:
            return 0.0  # 분석할 텍스트 없음

        results = sentiment_pipeline(texts)
        score = 0.0
        for result in results:
            label = result["label"].lower()
            if "positive" in label:
                score += 1
            elif "negative" in label:
                score -= 1
            # neutral은 0

        final_score = round(score / len(results), 2)
        return final_score

    except Exception as e:
        logging.error(f"❌ FinBERT 감정 분석 실패: {e}")
        print(f"⚠️ FinBERT 감정 분석 실패: {e}")
        return 0.0

# ✅ 테스트 실행
if __name__ == "__main__":
    score = analyze_finbert_sentiment()
    print(f"📈 FinBERT 커뮤니티 감정 점수: {score}")
