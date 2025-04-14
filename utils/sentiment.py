"""
📌 감정 분석 모듈 (한국어 룰 + 영어 BERT + 요약 해석 포함)
"""

from transformers import pipeline

# 영어 감정 분석용 pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_news(news_list):
    """
    뉴스 리스트 전체 감정 점수 평균 계산
    - 각 뉴스의 sentiment 필드에 점수 저장
    """
    scores = []
    for news in news_list:
        try:
            full_text = f"{news['title']} {news['summary']}"
            if news.get("language", "ko") == "en":
                score = analyze_single_news_en(full_text)
            else:
                score = analyze_single_news_ko(full_text)
            news["sentiment"] = score
            scores.append(score)
        except:
            continue

    return sum(scores) / len(scores) if scores else 0.0


def analyze_single_news_en(text):
    try:
        result = sentiment_pipeline(text)[0]
        label = result["label"]
        score = result["score"]
        return score if label == "POSITIVE" else -score
    except:
        return 0.0


def analyze_single_news_ko(text):
    negative_keywords = ["하락", "급락", "규제", "불안", "리스크", "패닉", "부정", "폭락", "제재", "손실"]
    positive_keywords = ["상승", "급등", "호재", "기대", "수익", "성장", "호황", "기록", "최고", "강세"]

    text = text.lower()
    score = 0
    for word in positive_keywords:
        if word in text:
            score += 0.5
    for word in negative_keywords:
        if word in text:
            score -= 0.5

    return max(-1.0, min(1.0, score))


def get_sentiment_summary(score: float) -> str:
    if score > 0.3:
        return "📈 긍정적 심리 우세 - 상승 가능성"
    elif score < -0.3:
        return "📉 부정적 심리 우세 - 하락 가능성"
    else:
        return "🔍 혼조 또는 중립 심리"
