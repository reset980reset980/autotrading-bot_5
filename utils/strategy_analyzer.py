# 📁 파일명: utils/strategy_analyzer.py
# 🎯 목적: 전략 판단 시스템의 핵심 모듈 (Grok + 보완 + 딥러닝 + 커뮤니티 반영)
# 🔄 전체 흐름도:
#   1. AI(Grok) 응답 기반 전략 해석
#   2. HOLD일 경우 상위 프레임 및 감정 기반 보완 전략 적용
#   3. 딥러닝 예측 결과 보조 반영
#   4. 커뮤니티 반응 기반 추가 필터링
# 📚 포함 함수:
#   - analyze_strategy()
#   - analyze_strategy_with_context()
#   - apply_model_correction()
#   - apply_community_adjustment()
# 💬 작업 프롬프트 요약:
#   ▶ "전략 판단 시, AI 응답 + 보완 판단 + 딥러닝 예측 + 커뮤니티 반응까지 종합적으로 판단하라."

from utils.indicators import get_indicators
from modules.grok_bridge import query_grok
from models.model_predictor import predict_with_model  # ✅ 딥러닝 예측 결과 가져오기
from modules.community_sentiment import analyze_community_sentiment  # ✅ 커뮤니티 반응 분석 모듈

def analyze_community_sentiment() -> float:
    """
    커뮤니티 감정 분석 결과를 반환합니다.
    현재는 임시로 고정 점수를 반환합니다.
    추후에는 실제 트위터/X 등에서 데이터를 수집해 분석하도록 확장 가능합니다.
    """
    # TODO: 실제 커뮤니티 분석 로직으로 대체
    return 0.1  # 예시: 약간 긍정적

def analyze_strategy(ai_response, indicators, sentiment_score):
    """
    Grok 응답으로부터 전략 판단 및 수치(TP/SL) 추출
    """
    try:
        lines = ai_response.splitlines()
        signal = "hold"
        tp = 0.0
        sl = 0.0

        for line in lines:
            if "LONG" in line:
                signal = "long"
            elif "SHORT" in line:
                signal = "short"
            elif "HOLD" in line:
                signal = "hold"
            elif "익절" in line or "Take Profit" in line:
                try:
                    tp = float(''.join(c for c in line if c.isdigit() or c == '.'))
                except:
                    tp = 0.0
            elif "손절" in line or "Stop Loss" in line:
                try:
                    sl = float(''.join(c for c in line if c.isdigit() or c == '.'))
                except:
                    sl = 0.0

        return {
            "signal": signal,
            "tp": tp if signal != "hold" else 0.0,
            "sl": sl if signal != "hold" else 0.0,
            "entry_price": indicators.get("close", 0)
        }, {
            "rsi": indicators.get("rsi"),
            "bb": indicators.get("bb"),
            "ema": indicators.get("ema"),
            "tema": indicators.get("tema"),
            "macd": indicators.get("macd"),
            "sentiment": sentiment_score,
            "summary": f"RSI: {indicators['rsi']}, BB 위치: {indicators['bb']}, 감정: {sentiment_score}, 다이버전스: {indicators.get('divergence', '없음')}"
        }

    except Exception as e:
        print(f"⚠️ 전략 분석 실패: {e}")
        return {
            "signal": "hold", "tp": 0.0, "sl": 0.0, "entry_price": 0.0
        }, {
            "summary": "전략 분석 실패", "sentiment": sentiment_score
        }


def analyze_strategy_with_context(sentiment_score: float, base_interval="15m") -> dict:
    """
    HOLD 응답 시 → 상위프레임 기반 보완 전략 판단
    """
    indicators_base = get_indicators("BTC/USDT", base_interval)
    indicators_1h = get_indicators("BTC/USDT", "1h")
    indicators_4h = get_indicators("BTC/USDT", "4h")

    prompt = f"""
    Technical Indicators:
    RSI: {indicators_base['rsi']}, BB: {indicators_base['bb']},
    EMA: {indicators_base['ema']}, TEMA: {indicators_base['tema']},
    MACD: {indicators_base['macd']}
    Market Sentiment: {sentiment_score}
    Based on the above, should we go LONG, SHORT, or HOLD?
    """

    try:
        ai_response = query_grok(prompt).strip().upper()
    except Exception as e:
        print(f"⚠️ Grok 호출 실패 (보완 전략): {e}")
        ai_response = "HOLD"

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

from utils.data_cleaner import run_strategy_safe as run_strategy
from utils.data_cleaner import get_strategy_summary_safe as get_strategy_summary

def apply_model_correction(signal: str, indicators: dict, sentiment_score: float) -> str:
    """
    딥러닝 모델 예측 결과를 활용하여 전략 신호 보정
    """
    model_pred = predict_with_model(indicators, sentiment_score)  # 예: "long", "short", "hold"
    if signal == "hold" and model_pred != "hold":
        print(f"🤖 딥러닝 보완 적용: {signal} → {model_pred}")
        return model_pred
    return signal


def apply_community_adjustment(signal: str) -> str:
    """
    커뮤니티 반응 기반 보완 판단
    """
    try:
        community_sentiment = analyze_community_sentiment()  # -1(부정), 0(중립), 1(긍정)
        if signal == "long" and community_sentiment == -1:
            print("👥 커뮤니티 반응: 부정 → LONG → HOLD 전환")
            return "hold"
        elif signal == "short" and community_sentiment == 1:
            print("👥 커뮤니티 반응: 긍정 → SHORT → HOLD 전환")
            return "hold"
        return signal
    except Exception as e:
        print(f"⚠️ 커뮤니티 분석 실패: {e}")
        return signal
