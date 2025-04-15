"""
📁 파일명: utils/sentiment.py
📌 목적: 뉴스 감정 분석 (제목 + 본문 포함, 다국어 대응)
🔧 변경 내역:
  - 영어 뉴스: FinBERT 모델 기반 감정 점수 계산
  - 한국어 뉴스: 키워드 기반 룰 엔진
  - 제목 + 요약을 함께 분석 텍스트로 사용
📊 포함 함수:
  - analyze_news(news_list): 전체 뉴스 리스트 분석, 평균 점수 반환
  - analyze_single_news_en(text): 영어 뉴스 감정 분석 (FinBERT)
  - analyze_single_news_ko(text): 한국어 뉴스 감정 분석 (룰기반)
  - get_sentiment_summary(score): 점수 기반 요약 텍스트 반환
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

# ✅ FinBERT 로드 (영어 금융 감정 분석 전용)
FINBERT_MODEL = "yiyanghkust/finbert-tone"
tokenizer = AutoTokenizer.from_pretrained(FINBERT_MODEL)
model = AutoModelForSequenceClassification.from_pretrained(FINBERT_MODEL)
finbert_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def analyze_news(news_list):
    """
    전체 뉴스 리스트를 기반으로 평균 감정 점수 계산
    """
    scores = []
    for news in news_list:
        try:
            lang = news.get("language", "ko")
            text = (news.get("title", "") + " " + news.get("summary", "")).strip()
            if lang == "en":
                score = analyze_single_news_en(text)
            else:
                score = analyze_single_news_ko(text)
            scores.append(score)
        except:
            continue

    if scores:
        return sum(scores) / len(scores)
    return 0.0

def analyze_single_news_en(text):
    """
    FinBERT 기반 영어 뉴스 감정 분석 → 점수화 (-1 ~ +1)
    """
    try:
        result = finbert_pipeline(text)[0]
        label = result["label"]
        score = result["score"]
        if label == "positive":
            return score
        elif label == "negative":
            return -score
        else:
            return 0.0  # neutral
    except:
        return 0.0

def analyze_single_news_ko(text):
    """
    한글 뉴스 감정 분석 (키워드 룰 기반)
    """
    negative_keywords = ["하락", "급락", "규제", "불안", "리스크", "패닉", "부정", "폭락", "제재", "손실"]
    positive_keywords = ["상승", "급등", "호재", "기대", "수익", "성장", "호황", "기록", "최고", "강세"]

    score = 0
    for word in positive_keywords:
        if word in text:
            score += 0.5
    for word in negative_keywords:
        if word in text:
            score -= 0.5

    return max(-1.0, min(1.0, score))

def get_sentiment_summary(score: float) -> str:
    """
    감정 점수 기반 요약 텍스트
    """
    if score > 0.3:
        return "📈 긍정적 심리 우세 - 상승 가능성"
    elif score < -0.3:
        return "📉 부정적 심리 우세 - 하락 가능성"
    else:
        return "🔍 혼조 또는 중립 심리"
