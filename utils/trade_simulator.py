# 📁 파일명: utils/trade_simulator.py
"""
📌 목적: 전략 결과에 기반한 가상 매매 시뮬레이션
📌 기능:
  - simulate_trade(): 전략 실행에 따른 수익 계산
  - record_trade_log(): 개별 매매 결과 저장
  - record_daily_summary(): 일일 누적 수익 요약 기록
📌 프롬프트 요약:
  ▶ "전략 결과를 받아 수익을 시뮬레이션하고, 일일 로그 및 수익률을 기록하라."
"""

import os
import json
from datetime import datetime

SIMULATION_LOG_PATH = "logs/simulation/simulated_trades.json"
DAILY_SUMMARY_PATH = "logs/daily_summaries"
INITIAL_BALANCE = 1_000_000

def load_trade_log():
    if not os.path.exists(SIMULATION_LOG_PATH):
        return []
    with open(SIMULATION_LOG_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def simulate_trade(signal: str, entry_price: float, tp: float, sl: float):
    if signal == "long":
        profit = entry_price * (tp / 100) - entry_price * (sl / 100)
    elif signal == "short":
        profit = entry_price * (sl / 100) - entry_price * (tp / 100)
    else:
        return 0.0
    return profit

def record_trade_log(entry: dict):
    logs = load_trade_log()
    logs.append(entry)
    logs = logs[-1000:]
    os.makedirs(os.path.dirname(SIMULATION_LOG_PATH), exist_ok=True)
    with open(SIMULATION_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

def record_daily_summary():
    logs = load_trade_log()
    os.makedirs(DAILY_SUMMARY_PATH, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    summary_path = os.path.join(DAILY_SUMMARY_PATH, f"{today}.txt")

    balance = INITIAL_BALANCE + sum(entry["profit"] for entry in logs if "profit" in entry)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"[{today}] 누적 수익 요약\n")
        f.write(f"시뮬레이션 잔고: {balance:,.2f}원\n")
        f.write(f"총 거래 수: {len(logs)}회\n")
