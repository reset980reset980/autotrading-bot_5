# 📁 파일명: evaluate_strategy_accuracy.py
# 🎯 목적: 예측된 신호와 실제 결과를 비교해 전략 판단 성능 수치 계산

import json
from modules.model_evaluator import evaluate_strategy_performance

def convert_to_label(signal: str) -> int:
    return 1 if signal == "long" else 0

def convert_to_actual(result: str) -> int:
    return 1 if "WIN" in result else 0

if __name__ == "__main__":
    path = "logs/simulation/simulated_trades_cleaned.json"
    with open(path, 'r', encoding='utf-8') as f:
        logs = json.load(f)

    predictions = []
    actuals = []

    for log in logs:
        if "signal" in log and "result" in log:
            predictions.append(convert_to_label(log["signal"]))
            actuals.append(convert_to_actual(log["result"]))

    metrics = evaluate_strategy_performance(predictions, actuals)

    print("📊 전략 성능 평가 지표:")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}" if value is not None else f"{key}: N/A")
