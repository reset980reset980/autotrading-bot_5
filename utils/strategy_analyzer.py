# utils/strategy_analyzer.py

def analyze_strategy(grok_response: str, indicators: dict, sentiment_score: float):
    """
    Grok 응답 기반으로 전략을 분석하여 signal, tp, sl, 전략 요약 반환
    """
    lower_grok = grok_response.lower()
    signal = "hold"
    if "long" in lower_grok and "short" not in lower_grok:
        signal = "long"
    elif "short" in lower_grok and "long" not in lower_grok:
        signal = "short"

    # 기본 손절/익절 비율
    tp = 1.2 if signal != "hold" else 0.0
    sl = 0.6 if signal != "hold" else 0.0

    # 전략 요약 구성
    bb_location = indicators.get("bb", "중앙")
    summary = []

    if indicators["rsi"] < 30:
        summary.append("과매도 (RSI < 20)")
    elif indicators["rsi"] > 70:
        summary.append("과매수 (RSI > 80)")
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

# ✅ 자동매매 시스템에서 호출할 최종 실행 함수
def run_strategy():
    # 샘플 입력값 (실제 시스템에서는 동적으로 제공 예정)
    grok_response = "AI는 현재 시장 상황을 강세로 판단하며 롱 포지션이 유리하다고 봅니다."
    indicators = {
        "rsi": 28.5,
        "bb": "하단",
        "ema": 27600,
        "tema": 27580,
        "macd": -24.2
    }
    sentiment_score = 0.35
    current_price = 27500  # ← 현재가 또는 예측 진입가 (entry_price로 제공)

    strategy, detail = analyze_strategy(grok_response, indicators, sentiment_score)

    return {
        **strategy,
        **detail,
        "entry_price": current_price  # ✅ 필수 키 추가
    }
