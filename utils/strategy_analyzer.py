# 📁 파일명: utils/strategy_analyzer.py
"""
📌 목적: 전략 판단 (AI 응답 + 기술 지표 + 감정 점수 기반)
📌 기능:
  - run_strategy(): 전략 판단 실행
  - analyze_strategy(): AI 응답 및 지표 조합으로 TP/SL 계산
  - get_strategy_summary(): 판단 결과 요약 반환
📌 작업 프롬프트 요약:
  ▶ "Grok 응답과 기술적 지표, 감정 분석을 통합해 전략을 판단하고, TP/SL을 함께 제공하라."
"""

from utils.indicators import get_indicators
from utils.sentiment import analyze_news
from modules.grok_bridge import query_grok
from utils.strategy_logic import analyze_strategy
from modules.ai_model import query_grok

def refine_signal_from_response(grok_response: str) -> str:
    """
    AI 응답에서 전략 신호를 명확하게 결정
    - long과 short가 함께 있어도, 추천 강도나 표현을 분석하여 방향 판단
    """
    lower = grok_response.lower()

    if "recommendation: short" in lower:
        return "short"
    if "recommendation: long" in lower:
        return "long"

    if "short seems more aligned" in lower:
        return "short"
    if "long seems more aligned" in lower:
        return "long"
    if "consider a short" in lower:
        return "short"
    if "consider a long" in lower:
        return "long"

    if "go short" in lower:
        return "short"
    if "go long" in lower:
        return "long"

    if "hold" in lower:
        return "hold"

    return "hold"


def analyze_strategy(grok_response: str, indicators: dict, sentiment_score: float):
    """
    Grok 응답 기반으로 전략을 분석하여 signal, tp, sl 반환
    """
    signal = refine_signal_from_response(grok_response)

    # 기본값
    tp = 1.2 if signal != "hold" else 0.0
    sl = 0.6 if signal != "hold" else 0.0

    # 전략 요약 정보
    bb_location = indicators.get("bb", "중앙")
    divergence = indicators.get("divergence", "없음")
    summary = []

    if indicators["rsi"] < 20:
        summary.append("과매도 (RSI < 20)")
    elif indicators["rsi"] > 80:
        summary.append("과매수 (RSI > 80)")
    else:
        summary.append("RSI 중립")

    summary.append(f"BB 위치: {bb_location}")
    summary.append("감정 긍정" if sentiment_score > 0.3 else "감정 부정" if sentiment_score < -0.3 else "감정 혼조")
    summary.append(f"다이버전스: {divergence}")

    return {
        "signal": signal,
        "tp": tp,
        "sl": sl,
        "entry_price": indicators.get("close", 0)
    }, {
        "rsi": indicators["rsi"],
        "bb": bb_location,
        "ema": indicators.get("ema", 0),
        "tema": indicators.get("tema", 0),
        "macd": indicators.get("macd", 0),
        "sentiment": sentiment_score,
        "summary": ", ".join(summary)
    }

def run_strategy():
    """
    전체 전략 실행: Grok 호출 + 실패 시 보조 전략 판단
    """
    indicators = get_indicators("BTC/USDT", "15m")
    news_list = analyze_news()
    sentiment_score = analyze_news(news_list)

    prompt = f"""
    Technical Indicators:
    RSI: {indicators['rsi']}, BB: {indicators['bb']}, EMA: {indicators['ema']}, TEMA: {indicators['tema']}, MACD: {indicators['macd']}
    Market Sentiment: {sentiment_score}
    Based on the above, should we go LONG, SHORT, or HOLD?
    """

    # 🔁 Grok 호출 + 1회 재시도
    ai_response = query_grok(prompt)
    if ai_response.strip().lower() in ["", "timeout", "error"]:
        ai_response = "HOLD"

    core, summary = analyze_strategy(ai_response, indicators, sentiment_score)

    # ✅ HOLD일 경우 보조 전략 판단 적용
    if core["signal"] == "hold":
        rsi = indicators["rsi"]
        bb = indicators["bb"]
        macd = indicators["macd"]
        if rsi > 70 and bb == "상단" and sentiment_score < -0.2:
            core["signal"] = "short"
            core["tp"] = 1.0
            core["sl"] = 0.5
        elif rsi < 30 and bb == "하단" and sentiment_score > 0.2:
            core["signal"] = "long"
            core["tp"] = 1.2
            core["sl"] = 0.6

    return {**core, **summary}