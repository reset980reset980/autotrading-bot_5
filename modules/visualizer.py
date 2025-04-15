"""
파일명: visualizer.py
📌 목적:
  - 감정 분석 결과와 전략 판단 흐름을 시간대별로 시각화하여 사용자에게 제공
  - Streamlit 기반 대시보드에서 사용

📊 기능:
  - 감정 점수 시계열 꺾은선 그래프
  - 전략 판단 흐름 (롱/숏/홀드) 타임라인 표시
  - RSI, MACD 등 기술 지표 시각적 비교 (선택적으로 추가 가능)

📦 의존 라이브러리:
  - matplotlib
  - pandas

🧠 작업 프롬프트:
  ▶ "전략 판단 결과를 시간 순서대로 정렬하고, 감정 점수와 전략 신호를 시각적으로 표현하여 사용자가 흐름을 직관적으로 이해할 수 있도록 하라."
"""

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st

def plot_sentiment_trend(data: list):
    """
    📈 감정 점수 시계열 그래프 (시간대별 감정 흐름)
    """
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])

    plt.figure(figsize=(10, 4))
    plt.plot(df['time'], df['sentiment'], marker='o', linestyle='-')
    plt.title("📊 시간대별 감정 점수 변화")
    plt.xlabel("시간")
    plt.ylabel("감정 점수")
    plt.axhline(y=0, color='gray', linestyle='--')
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

    """
📌 예시: 시각화용 함수 템플릿 (Streamlit + Plotly 기반)
    """
def visualize_sentiment_over_time(news_list):
    """
    시간대별 뉴스 감정 점수 변화 시각화 (Plotly)
    """
    if not news_list:
        st.warning("분석할 뉴스가 없습니다.")
        return

    df = pd.DataFrame([
        {
            "time": news.get("timestamp"),
            "score": news.get("sentiment", 0.0)
        }
        for news in news_list if news.get("timestamp")
    ])

    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time")

    fig = px.line(df, x="time", y="score", title="🧠 시간대별 뉴스 감정 추이", markers=True)
    fig.update_layout(yaxis_title="감정 점수 (-1 ~ +1)", xaxis_title="시간")

    st.plotly_chart(fig, use_container_width=True)
    

def plot_strategy_signals(data: list):
    """
    🚦 전략 신호 시각화 (롱/숏/홀드 타임라인)
    """
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])

    color_map = {'long': 'green', 'short': 'red', 'hold': 'gray'}
    marker_map = {'long': '^', 'short': 'v', 'hold': 'o'}

    plt.figure(figsize=(10, 4))
    for idx, row in df.iterrows():
        color = color_map.get(row['signal'], 'gray')
        marker = marker_map.get(row['signal'], 'o')
        plt.scatter(row['time'], 0, color=color, marker=marker, s=100, label=row['signal'] if idx == 0 else "")
    
    plt.title("📌 전략 흐름 (롱/숏/홀드)")
    plt.yticks([])
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_indicators(data: list):
    """
    📊 RSI, MACD 시계열 그래프
    """
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
