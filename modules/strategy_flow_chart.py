# 📁 파일명: modules/strategy_flow_chart.py
# 🎯 목적: 전략 판단 과정에서의 signal, sentiment, 기술 지표 흐름을 시계열 그래프로 시각화
# 🧭 전체 흐름도:
#     - 시뮬레이션 또는 실매매 결과를 시간순으로 불러옴
#     - signal 변화, sentiment 점수, RSI 등 지표들을 선 그래프로 시각화
# 📈 주요 함수:
#     - load_trade_logs(): 최근 거래 데이터 로드
#     - plot_strategy_flow(): 판단 흐름 그래프 출력
# 📍 프롬프트 요약:
#     ▶ "시간 흐름에 따른 전략 방향, 감정 점수, RSI 등을 시각적으로 표시하여 흐름을 확인할 수 있게 구성하라."

import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def load_trade_logs(filepath="logs/simulation/simulated_trades.json", limit=50):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data[-limit:])  # 최근 50개만

def plot_strategy_flow(df: pd.DataFrame):
    df["time"] = pd.to_datetime(df["timestamp"] if "timestamp" in df else df["time"])
    df = df.sort_values("time")

    # 전략 방향 수치화
    df["signal_num"] = df["signal"].map({"long": 1, "hold": 0, "short": -1})

    plt.figure(figsize=(12, 6))
    plt.plot(df["time"], df["signal_num"], marker='o', label="Signal (long=1, short=-1)")
    plt.plot(df["time"], df["sentiment"], label="Sentiment Score", linestyle="--")
    plt.plot(df["time"], df["rsi"], label="RSI", linestyle=":")

    plt.axhline(0, color="gray", linestyle="--", linewidth=0.5)
    plt.axhline(70, color="red", linestyle="--", linewidth=0.5)
    plt.axhline(30, color="blue", linestyle="--", linewidth=0.5)

    plt.legend()
    plt.title("전략 판단 흐름 차트")
    plt.xlabel("시간")
    plt.ylabel("지표 값")
    plt.tight_layout()
    plt.grid(True)
    plt.show()

# ✅ 단독 실행 예시
if __name__ == "__main__":
    df = load_trade_logs()
    plot_strategy_flow(df)
