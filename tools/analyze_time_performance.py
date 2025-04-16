# 📁 파일명: analyze_time_performance.py
# 🎯 목적: 정제된 로그 기반 시간대별 전략 성능 분석 결과 콘솔에 출력

import json
from modules.time_impact_analyzer import analyze_by_hour

def load_logs(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

if __name__ == "__main__":
    log_path = "logs/simulation/simulated_trades_cleaned.json"
    logs = load_logs(log_path)

    summary = analyze_by_hour(logs)

    print("🕒 시간대별 전략 성능 요약:")
    for hour in sorted(summary.keys()):
        data = summary[hour]
        print(f"{hour:02d}시 ➤ 승률: {data['win_rate']*100:.1f}%, 거래 수: {data['trade_count']}, 평균 수익률: {data['avg_profit']}")
