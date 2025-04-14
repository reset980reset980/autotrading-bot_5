# utils/grok_bridge.py
"""
🤖 Grok 또는 GPT 기반 전략 분석 모듈
- 기술 지표 + 감정 점수 + 뉴스 제목 기반으로 전략 분석 요청
- OpenAI(gpt-4 또는 grok)를 사용해 응답 처리
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ openai>=1.0.0 구조 반영

def get_grok_response(indicators: dict, sentiment_score: float, news_data: list) -> dict:
    """
    📡 기술 지표 및 감정 분석 결과를 기반으로 Grok/GPT에게 전략 분석 요청

    Parameters:
        indicators (dict): RSI, MACD, EMA, TEMA 등 기술지표 값
        sentiment_score (float): 전체 감정 점수
        news_data (list): 주요 뉴스 제목 리스트

    Returns:
        dict: Grok 또는 GPT 응답
    """

    prompt = f"""
📊 다음은 암호화폐 시장에 대한 분석 정보입니다. 이 정보를 바탕으로 매매 전략을 제시해주세요.

- RSI: {indicators.get("rsi")}
- MACD: {indicators.get("macd")}
- EMA: {indicators.get("ema")}
- TEMA: {indicators.get("tema")}
- 감정 점수(시장 심리): {sentiment_score}

📰 뉴스 헤드라인:
{chr(10).join(['- ' + news['title'] for news in news_data])}

🧠 판단 요청:
당신은 최고의 트레이딩 전문가입니다. 위의 지표와 시장 뉴스를 기반으로 아래 형식에 맞춰 전략을 제시해주세요.

반드시 다음 형식을 따르세요:
1. 매매 방향: (long / short / hold 중 선택)
2. 전략 요약: (한 줄 설명)
3. 근거 요약: (지표 및 뉴스 기반 근거를 요약 정리)

결과는 한국어로 답해주세요.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 암호화폐 전문 트레이더입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return {"text": response.choices[0].message.content.strip()}

    except Exception as e:
        print("⚠️ Grok 응답 오류:", e)
        return {"text": "⚠️ Grok 응답 실패"}
