# 📁 파일명: utils/strategy_analyzer.py
# 🎯 목적: 전체 전략 판단 로직 통합 (Grok 응답, 딥러닝 예측, 커뮤니티 기반 보정 포함)
# 🔄 전체 흐름:
#     - 기술 지표 + 감정 점수 분석
#     - Grok AI 판단 결과 해석
#     - HOLD 시 보완 전략 (상위 프레임)
#     - 딥러닝 예측 기반 보정
#     - 커뮤니티 반응 기반 필터링
# 📚 주요 함수:
#     - analyze_strategy()
#     - analyze_strategy_with_context()
#     - apply_model_correction()
#     - apply_community_adjustment()

from utils.indicators import get_indicators
from models.model_predictor import predict_with_model, update_sequence
from modules.grok_bridge import query_grok
from modules.community_sentiment import analyze_community_sentiment

# ✅ Grok 응답 해석
def analyze_strategy(ai_response: str, indicators: dict, sentiment_score: float) -> tuple:
    signal = "hold"
    tp = 0.0
    sl = 0.0
    try:
        for line in ai_response.splitlines():
            line = line.strip().lower()
            if "long" in line:
                signal = "long"
            elif "short" in line:
                signal = "short"
            elif "hold" in line:
                signal = "hold"
            if "익절" in line or "take profit" in line:
                tp = float(''.join(c for c in line if c.isdigit() or c == '.'))
            if "손절" in line or "stop loss" in line:
                sl = float(''.join(c for c in line if c.isdigit() or c == '.'))
    except Exception as e:
        print(f"⚠️ 응답 해석 오류: {e}")

    entry_price = indicators.get("close", 0)
    return {
        "signal": signal,
        "tp": tp if signal != "hold" else 0.0,
        "sl": sl if signal != "hold" else 0.0,
        "entry_price": entry_price,
    }, {
        "rsi": indicators.get("rsi"),
        "bb": indicators.get("bb"),
        "ema": indicators.get("ema"),
        "tema": indicators.get("tema"),
        "macd": indicators.get("macd"),
        "sentiment": sentiment_score,
        "summary": f"RSI: {indicators['rsi']}, BB: {indicators['bb']}, 감정: {sentiment_score}, 다이버전스: {indicators.get('divergence', '없음')}"
    }

# ✅ 상위 프레임 보완 전략
def analyze_strategy_with_context(sentiment_score: float, base_interval="15m") -> dict:
    indicators_base = get_indicators("BTC/USDT", base_interval)
    indicators_1h = get_indicators("BTC/USDT", "1h")
    indicators_4h = get_indicators("BTC/USDT", "4h")

    prompt = f"""
[Analyze and respond in Korean]

기술적 지표:
RSI: {indicators_base['rsi']}, BB: {indicators_base['bb']},
EMA: {indicators_base['ema']}, TEMA: {indicators_base['tema']},
MACD: {indicators_base['macd']}
시장 심리 점수: {sentiment_score}

이 데이터를 기반으로 LONG / SHORT / HOLD 중 적절한 전략을 판단해줘.
"""
    ai_response = query_grok(prompt).strip().upper()

    signal = "hold"
    if ai_response in ["LONG", "SHORT"]:
        short_term_signal = ai_response.lower()
        higher_trend = indicators_1h.get("macd", 0) > 0 and indicators_4h.get("macd", 0) > 0
        lower_trend = indicators_1h.get("macd", 0) < 0 and indicators_4h.get("macd", 0) < 0
        if (short_term_signal == "long" and higher_trend) or (short_term_signal == "short" and lower_trend):
            signal = short_term_signal
        else:
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
        "summary": f"보완 전략 | RSI: {indicators_base['rsi']}, MACD: {indicators_base['macd']}, 감정: {sentiment_score}"
    }

# ✅ 딥러닝 기반 전략 보정
def apply_model_correction(signal: str, indicators: dict, sentiment: float) -> str:
    update_sequence({
        "rsi": indicators.get("rsi"),
        "macd": indicators.get("macd"),
        "ema": indicators.get("ema"),
        "tema": indicators.get("tema"),
        "sentiment": sentiment
    })

    model_signal = predict_with_model()
    print(f"🧠 딥러닝 판단: {model_signal}")

    return model_signal if model_signal != "hold" else signal

# ✅ 커뮤니티 감정 기반 필터링
def apply_community_adjustment(signal: str) -> str:
    community_score = analyze_community_sentiment("BTC")
    print(f"📣 커뮤니티 감정 점수: {community_score:.2f}")

    if signal == "long" and community_score < -0.3:
        print("🛑 커뮤니티 부정적 → long 차단")
        return "hold"
    elif signal == "short" and community_score > 0.3:
        print("🛑 커뮤니티 긍정적 → short 차단")
        return "hold"
    return signal
