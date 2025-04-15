# 📁 파일명: modules/community_sentiment.py
# 🎯 목적: 커뮤니티(X, Reddit 등) 기반 시장 감정 점수 분석 (확장 버전)
# 📌 주요 기능:
#     - snscrape 사용해 트위터 데이터 수집
#     - HuggingFace의 FinBERT 모델로 감정 분석
#     - 최근 커뮤니티 반응의 평균 감정 점수 반환
# ⚠️ 사용 전 설치 필요:
#     pip install snscrape transformers torch
#     또는 huggingface에서 다른 금융 감정 모델 대체 가능

import snscrape.modules.twitter as sntwitter
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from typing import List

# ✅ FinBERT 모델 로딩 (감정 분석)
MODEL_NAME = "yiyanghkust/finbert-tone"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

def fetch_tweets(keyword: str = "bitcoin", limit: int = 20) -> List[str]:
    """
    ▶ 최근 커뮤니티 글(Twitter 기준) 수집
    Args:
        keyword (str): 검색 키워드
        limit (int): 최대 수집 수
    Returns:
        List[str]: 텍스트 목록
    """
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(f'{keyword} lang:en').get_items():
        if len(tweets) >= limit:
            break
        tweets.append(tweet.content)
    return tweets

def analyze_sentiment_finbert(texts: List[str]) -> float:
    """
    ▶ 수집한 글을 FinBERT로 감정 분석
    Args:
        texts (List[str]): 분석할 텍스트 목록
    Returns:
        float: 전체 평균 감정 점수 (-1 ~ 1)
    """
    scores = []
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
            # FinBERT: [neutral, positive, negative]
            score = probs[1] - probs[2]  # 긍정 - 부정
            scores.append(score.item())

    if not scores:
        return 0.0
    return float(np.clip(np.mean(scores), -1.0, 1.0))

def analyze_community_sentiment(keyword: str = "bitcoin") -> float:
    """
    ✅ 통합 커뮤니티 감정 분석 함수
    Returns:
        float: 커뮤니티 감정 점수 (-1.0 ~ 1.0)
    """
    try:
        tweets = fetch_tweets(keyword=keyword, limit=30)
        score = analyze_sentiment_finbert(tweets)
        return round(score, 3)
    except Exception as e:
        print(f"⚠️ 커뮤니티 감정 분석 실패: {e}")
        return 0.0
