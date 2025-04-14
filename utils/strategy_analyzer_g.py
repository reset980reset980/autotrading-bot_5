# utils/strategy_analyzer_g.py (수정)
from googletrans import Translator

def translate_to_korean(text: str) -> str:
    translator = Translator()
    return translator.translate(text, dest="ko").text

def analyze_strategy(ai_response: str, indicators: dict, sentiment: float):
    signal = "hold"
    if "long" in ai_response.lower():
        signal = "long"
    elif "short" in ai_response.lower():
        signal = "short"

    tp = 1.5 if signal != "hold" else 0.0
    sl = 0.7 if signal != "hold" else 0.0

    translated_summary = translate_to_korean(ai_response)

    strategy = {
        "signal": signal,
        "tp": tp,
        "sl": sl
    }

    details = {
        "rsi": indicators["rsi"],
        "ema": indicators["ema"],
        "tema": indicators["tema"],
        "macd": indicators["macd"],
        "bb": indicators["bb"],
        "sentiment_score": sentiment,
        "summary": translated_summary
    }

    return strategy, details