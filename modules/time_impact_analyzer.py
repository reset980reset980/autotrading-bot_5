# 📁 파일명: modules/time_impact_analyzer.py
# 🎯 목적: 시간대별 전략 성능(승률, 수익률 등)을 분석하여 최적 매매 시간 도출
# 🔁 전체 흐름도:
#     - 거래 로그를 시간(HH) 단위로 그룹화
#     - 승률, 평균 수익률 등 산출
#     - 시각화 또는 전략 판단 최적 시간대 추론에 활용
# 🔧 주요 함수:
#     - analyze_by_hour(): 시간대별 요약 통계 반환
# 💬 작업 프롬프트 요약:
#     ▶ "하루 중 어느 시간대에 전략 성능이 좋은지 분석하라."

import pandas as pd
from collections import defaultdict
from typing import List, Dict

def analyze_by_hour(trade_logs: List[Dict]) -> Dict[int, Dict]:
    """
    거래 기록을 시간대별로 분석하여 전략 성능 통계를 반환합니다.

    Args:
        trade_logs (List[Dict]): 전략 실행 로그
            예: [{"timestamp": "2025-04-14T02:15:00", "result": "✅ WIN", "profit": 42.5}, ...]

    Returns:
        Dict[int, Dict]: 시간(HH)별 성능 요약 {hour: {"win_rate": float, "avg_profit": float, "trade_count": int}}
    """
    hourly_stats = defaultdict(lambda: {"wins": 0, "losses": 0, "count": 0, "total_profit": 0.0})

    for trade in trade_logs:
        time_str = trade.get("timestamp")
        try:
            hour = pd.to_datetime(time_str).hour
        except Exception:
            continue

        result = trade.get("result", "")
        profit = trade.get("profit", 0.0)

        hourly_stats[hour]["count"] += 1
        hourly_stats[hour]["total_profit"] += profit

        if "WIN" in result:
            hourly_stats[hour]["wins"] += 1
        elif "LOSS" in result:
            hourly_stats[hour]["losses"] += 1

    summary = {}
    for hour, stats in hourly_stats.items():
        count = stats["count"]
        winrate = stats["wins"] / count if count > 0 else 0.0
        avg_profit = stats["total_profit"] / count if count > 0 else 0.0

        summary[hour] = {
            "win_rate": round(winrate, 3),
            "trade_count": count,
            "avg_profit": round(avg_profit, 2)
        }

    return summary


# ✅ 예시 사용
if __name__ == "__main__":
    sample_logs = [
        {"timestamp": "2025-04-14T02:15:00", "result": "✅ WIN", "profit": 42.5},
        {"timestamp": "2025-04-14T02:45:00", "result": "❌ LOSS", "profit": -20.0},
        {"timestamp": "2025-04-14T14:00:00", "result": "✅ WIN", "profit": 70.0},
    ]
    result
