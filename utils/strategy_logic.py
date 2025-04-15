# utils/strategy_logic.py
"""
📌 전략 판단 보조 모듈
- Grok AI 응답을 해석하여 전략 판단 (LONG / SHORT / HOLD)
- 기술 지표 및 감정 점수를 바탕으로 판단 요약 생성
# 📁 파일명: utils/strategy_logic.py
# 🎯 목적: 15분봉 전략 판단 시, 상위 프레임(1h, 4h) 지표 및 감정 급등 여부 고려
# ✅ 업데이트: 상위 프레임 방향과 다를 경우 HOLD 또는 예외적 진입 판단

"""

from utils.indicators import get_indicators
from modules.grok_bridge import query_grok

def analyze_strategy_with_context(sentiment_score: float, base_interval="15m") -> dict:
    """
    전략 판단을 수행하고 상위 프레임을 참고하여 HOLD 예외 여부 판단
    """
    # 1. 기본 프레임 지표 (15m)
    indicators_base = get_indicators("BTC/USDT", base_interval)

    # 2. 상위 프레임 지표 (1h, 4h)
    indicators_1h = get_indicators("BTC/USDT", "1h")
    indicators_4h = get_indicators("BTC/USDT", "4h")

    # 3. 전략 판단용 프롬프트
    prompt = f"""
    Technical Indicators:
    RSI: {indicators_base['rsi']}, BB: {indicators_base['bb']},
    EMA: {indicators_base['ema']}, TEMA: {indicators_base['tema']},
    MACD: {indicators_base['macd']}
    Market Sentiment: {sentiment_score}
    Based on the above, should we go LONG, SHORT, or HOLD?
    """

    ai_response = query_grok(prompt).strip().upper()

    # 4. 신호 결정
    signal = "hold"
    if ai_response in ["LONG", "SHORT"]:
        short_term_signal = ai_response.lower()
        higher_trend = indicators_1h.get("macd", 0) > 0 and indicators_4h.get("macd", 0) > 0
        lower_trend = indicators_1h.get("macd", 0) < 0 and indicators_4h.get("macd", 0) < 0

        # 상하위 방향 일치 → 그대로 적용
        if (short_term_signal == "long" and higher_trend) or (short_term_signal == "short" and lower_trend):
            signal = short_term_signal
        else:
            # 지표 급변 or 감정 강한 경우 예외 적용
            macd_strength = abs(indicators_base.get("macd", 0))
            if macd_strength > 30 or abs(sentiment_score) > 0.6:
                signal = short_term_signal
            else:
                signal = "hold"
    else:
        signal = "hold"

    return {
        "signal": signal,
        "tp": 1.5 if signal != "hold" else 0.0,
        "sl": 0.5 if signal != "hold" else 0.0,
        "entry_price": indicators_base.get("close", 0),
        "rsi": indicators_base.get("rsi"),
        "bb": indicators_base.get("bb"),
        "ema": indicators_base.get("ema"),
        "tema": indicators_base.get("tema"),
        "macd": indicators_base.get("macd"),
        "sentiment": sentiment_score,
        "summary": f"RSI: {indicators_base['rsi']}, BB 위치: {indicators_base['bb']}, 감정: {sentiment_score}, 다이버전스: {indicators_base.get('divergence', '없음')}"
    }
