# 📁 파일명: modules/visualizer.py
# 🎯 목적: Matplotlib 기반 시각화 모듈

import matplotlib.pyplot as plt
import pandas as pd

def plot_sentiment_trend(data: list):
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])

    plt.figure(figsize=(10, 4))
    plt.plot(df['time'], df['sentiment'], marker='o', linestyle='-')
    plt.title("📊 시간대별 감정 점수 변화")
    plt.axhline(y=0, color='gray', linestyle='--')
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

def plot_strategy_signals(data: list):
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])

    color_map = {'long': 'green', 'short': 'red', 'hold': 'gray'}
    marker_map = {'long': '^', 'short': 'v', 'hold': 'o'}

    plt.figure(figsize=(10, 4))
    for idx, row in df.iterrows():
        plt.scatter(row['time'], 0, color=color_map.get(row['signal'], 'gray'),
                    marker=marker_map.get(row['signal'], 'o'), s=100)
    plt.title("📌 전략 흐름 (롱/숏/홀드)")
    plt.yticks([])
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_hourly_performance(hourly_summary: dict):
    hours = sorted(hourly_summary.keys())
    win_rates = [hourly_summary[h]["win_rate"] * 100 for h in hours]
    avg_profits = [hourly_summary[h]["avg_profit"] for h in hours]

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.bar(hours, avg_profits, alpha=0.6, label='평균 수익률')
    ax2 = ax1.twinx()
    ax2.plot(hours, win_rates, color='orange', marker='o', label='승률(%)')
    plt.title("🕒 시간대별 전략 성능")
    fig.legend(loc="upper left")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
def plot_indicators(data: list):
    """
    📊 RSI, MACD 시계열 그래프
    """
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])

    fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    axs[0].plot(df['time'], df['rsi'], color='blue', label='RSI')
    axs[0].axhline(70, color='red', linestyle='--', linewidth=0.8)
    axs[0].axhline(30, color='green', linestyle='--', linewidth=0.8)
    axs[0].set_title("📉 RSI 지표")
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(df['time'], df['macd'], color='purple', label='MACD')
    axs[1].axhline(0, color='gray', linestyle='--', linewidth=0.8)
    axs[1].set_title("📈 MACD 지표")
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()
    
