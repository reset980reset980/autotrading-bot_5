# 📁 파일명: modules/logger.py
# 🎯 목적: 매매 전략 판단 결과 및 실제 거래 로그를 파일로 저장
# 🔄 전체 흐름도:
#     - 매매 실행 결과를 시간별로 기록
#     - 하루 단위 요약 정리 파일 별도 저장
# 📚 주요 함수:
#     - log_trade_result(): 전략 결과 단건 로그 저장
#     - log_daily_summary(): 일별 수익 요약 정리
#     - save_json_log(): 시뮬레이션/실매매 결과 JSON 형태로 기록
# 💬 작업 프롬프트 요약:
#     ▶ "전략 실행 시점, 수익률, 신호, 감정 분석 결과를 모두 로컬 로그 파일로 저장하고, 하루 단위 요약도 함께 생성하라."

import os
import json
from datetime import datetime

TRADE_LOG_PATH = "logs/trade_log.txt"
SUMMARY_PATH = "logs/daily_summary.txt"
JSON_LOG_PATH = "logs/simulation/simulated_trades.json"

def log_trade_result(entry: dict, result: dict):
    os.makedirs("logs", exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(TRADE_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{now}] 전략: {entry['signal'].upper()} | TP: {entry['tp']}% | SL: {entry['sl']}% | RSI: {entry['rsi']} | 감정: {entry['sentiment']} | 결과: {result['result']}\n")

def log_daily_summary(entry: dict, balance: float):
    today = datetime.now().strftime("%Y-%m-%d")
    with open(SUMMARY_PATH, "a", encoding="utf-8") as f:
        f.write(f"{today} | 전략: {entry['signal']} | 수익률: {entry['pnl']} | 누적 잔고: {balance}\n")

def save_json_log(entry: dict):
    os.makedirs(os.path.dirname(JSON_LOG_PATH), exist_ok=True)
    try:
        with open(JSON_LOG_PATH, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except:
        logs = []

    entry["timestamp"] = datetime.now().isoformat()
    logs.append(entry)
    logs = logs[-1000:]  # 최근 1000개만 유지

    with open(JSON_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

# ✅ 예시
if __name__ == "__main__":
    test_entry = {
        "signal": "long", "tp": 1.5, "sl": 0.5, "rsi": 29.2, "sentiment": 0.4, "pnl": 23.0
    }
    test_result = {
        "result": "✅ WIN"
    }
    log_trade_result(test_entry, test_result)
    log_daily_summary(test_entry, balance=1023000.0)
    save_json_log({**test_entry, **test_result})
