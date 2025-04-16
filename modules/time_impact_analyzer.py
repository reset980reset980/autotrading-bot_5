# modules/time_impact_analyzer.py

import pandas as pd
from collections import defaultdict

def analyze_by_hour(trade_logs: list) -> dict:
    """
    시간대별 전략 성능 분석을 수행합니다.

    Args:
        trade_logs (list[dict]): 매매 기록 리스트. 각 항목은 다음을 포함:
            {
                "timestamp": "2025-04-14T02:15:00",
                "signal": "long",
                "result": "✅ WIN" or "❌ LOSS",
                "profit": 30.0
            }

    Returns:
        dict: 시간(HH) 단위로 묶은 승률, 거래 수, 평균 수익률
    """
    hourly_stats = defaultdict(lambda: {"wins": 0, "losses": 0, "count": 0, "total_profit": 0})

    for trade in trade_logs:
        time_str = trade.get("timestamp")
        if not time_str:
            continue

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

    # 계산 정리
    summary = {}
    for hour, stats in hourly_stats.items():
        winrate = stats["wins"] / stats["count"] if stats["count"] else 0
        avg_profit = stats["total_profit"] / stats["count"] if stats["count"] else 0

        summary[hour] = {
            "win_rate": round(winrate, 3),
            "trade_count": stats["count"],
            "avg_profit": round(avg_profit, 2)
        }

    return summary
