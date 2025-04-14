def analyze_strategy(grok_response: str, indicators: dict, sentiment_score: float):
    """
    Grok 응답 기반으로 전략을 분석하여 signal, tp, sl 반환
    """
    lower_grok = grok_response.lower()
    signal = "hold"
    if "long" in lower_grok and "short" not in lower_grok:
        signal = "long"
    elif "short" in lower_grok and "long" not in lower_grok:
        signal = "short"

    # 기본값
    tp = 1.2 if signal != "hold" else 0.0
    sl = 0.6 if signal != "hold" else 0.0

    # 전략 요약 정보
    bb_location = indicators.get("bb", "중앙")
    summary = []

    if indicators["rsi"] < 30:
        summary.append("과매도 (RSI < 30)")
    elif indicators["rsi"] > 70:
        summary.append("과매수 (RSI > 70)")
    else:
        summary.append("RSI 중립")

    summary.append(f"BB 위치: {bb_location}")
    summary.append("감정 긍정" if sentiment_score > 0.3 else "감정 부정" if sentiment_score < -0.3 else "감정 혼조")

    return {
        "signal": signal,
        "tp": tp,
        "sl": sl
    }, {
        "rsi": indicators["rsi"],
        "bb": bb_location,
        "ema": indicators.get("ema", 0),
        "tema": indicators.get("tema", 0),
        "macd": indicators.get("macd", 0),
        "sentiment": sentiment_score,
        "summary": ", ".join(summary)
    }
