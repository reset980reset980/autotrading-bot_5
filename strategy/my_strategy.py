import random

def run_strategy():
    # 예시용 임의 전략 결과 생성
    return {
        "signal": random.choice(["long", "short"]),
        "entry_price": 65000,
        "tp": 66500,
        "sl": 64500,
        "confidence": round(random.uniform(0.6, 0.95), 2),
        "rsi": round(random.uniform(30, 70), 2),
        "sentiment_score": round(random.uniform(-1, 1), 2)
    }
