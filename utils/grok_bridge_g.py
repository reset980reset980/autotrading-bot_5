# utils/grok_bridge_g.py
import json
from utils.indicators_g import get_indicators
from utils.news_fetcher_g import fetch_news
from utils.sentiment_g import analyze_news

def get_grok_response(indicators, sentiment_score, news_data):
    news_summary = "\n".join(
        f"- {item['title']} ({item['source']}): {item['published']}"
        for item in news_data
    )
    
    # Series 객체에서 최신 값을 추출
    rsi_latest = indicators['rsi'].iloc[-1]
    ema_latest = indicators['ema'].iloc[-1]
    tema_latest = indicators['tema'].iloc[-1]
    macd_latest = indicators['macd'].iloc[-1]
    
    prompt = f"""
다음은 암호화폐 기술 지표와 뉴스 감정 점수입니다. 이 정보를 기반으로 매매 전략을 추천해주세요.

📈 기술 지표:
- RSI: {rsi_latest:.2f}
- EMA: {ema_latest:.2f}
- TEMA: {tema_latest:.2f}
- MACD: {macd_latest:.2f}
- 볼린저 밴드: {indicators['bb']}
- 다이버전스: {indicators['divergence']}

📊 뉴스 감정 점수: {sentiment_score}

📰 최근 뉴스:
{news_summary}

위 정보를 바탕으로 매매 전략을 추천해주세요. 추천 전략은 다음과 같은 형식으로 작성해 주세요:
- signal: "long" 또는 "short"
- tp: 익절 비율 (숫자, 단위: %)
- sl: 손절 비율 (숫자, 단위: %)
- reason: 전략 추천 이유 (문자열)
- summary: 요약 (문자열)

JSON 형식으로 응답해 주세요.
"""
    print(f"Raw prompt: {prompt}")
    
    # Grok API 호출 (임시로 더미 응답 반환)
    response = {
        "text": json.dumps({
            "signal": "long",
            "tp": 2.5,
            "sl": 1.0,
            "reason": "RSI가 낮고, 감정 점수 중립적",
            "summary": "매수 추천"
        }),
        "token_usage": 100
    }
    print(f"Raw API response: {response['text']}")
    return response