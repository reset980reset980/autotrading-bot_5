# Sample Python module

def example():
    print('This is a sample.')
# 📁 파일명: utils/summary_generator.py
"""
📌 목적: 매일의 전략 실행 결과를 요약 정리하여 파일 또는 텔레그램 등으로 제공
📌 기능:
  - generate_daily_summary(): 오늘의 거래 요약 텍스트 생성
  - get_simulation_performance(): 누적 수익률, 승률 등 통계 계산
📌 프롬프트 요약:
  ▶ "시뮬레이션 거래 로그를 바탕으로 당일 전략 요약과 누적 통계를 정리하여 출력하는 유틸리티 구성"
"""

import os
import json
from datetime import datetime

SIM_LOG_PATH = "logs/simulation/simulated_trades.json"

def load_trade_log():
    if not os.path.exists(SIM_LOG_PATH):
        return []
    with open(SIM_LOG_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def generate_daily_summary():
    logs = load_trade_log()
    today = datetime.now().strftime("%Y-%m-%d")
    today_logs = [entry for entry in logs if entry["timestamp"].startswith(today)]

    if not today_logs:
        return "📭 오늘의 거래가 없습니다."

    summary_lines = [f"📅 오늘의 거래 요약 ({today})"]

    for entry in today_logs:
        summary_lines.append(f"- [{entry['timestamp'][11:16]}] {entry['signal']} | 수익: ${entry['profit']:.2f}")

    stats = get_simulation_performance(logs)
    summary_lines.append("")
    summary_lines.append(f"📊 누적 수익: ${stats['total_profit']:.2f}")
    summary_lines.append(f"✅ 승률: {stats['win_rate']}% ({stats['wins']}승 / {stats['total']}회)")

    return "\n".join(summary_lines)

def get_simulation_performance(logs: list):
    total_profit = 0.0
    wins = 0
    total = 0

    for entry in logs:
        profit = entry.get("profit", 0)
        total_profit += profit
        if profit > 0:
            wins += 1
        total += 1

    win_rate = round((wins / total) * 100, 1) if total > 0 else 0.0
    return {
        "total_profit": total_profit,
        "wins": wins,
        "total": total,
        "win_rate": win_rate
    }
