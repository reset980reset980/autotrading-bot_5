# 📁 파일명: modules/streamlit_visualizer.py
# 🎯 목적: Streamlit 환경에서 감정 분석 결과를 시각화하는 전용 모듈
# 기능 요약:
#   - 뉴스 감정 점수 시계열 그래프 (Plotly)
#   - 향후: 전략 흐름 시각화, 실시간 지표 시각화 가능 확장

import streamlit as st
import plotly.express as px
import pandas as pd

def visualize_sentiment_over_time(news_list):
    """
    🧠 시간대별 뉴스 감정 점수 시각화 (Plotly + Streamlit)
    Args:
        news_list (list): 뉴스 항목 리스트 [{"timestamp": ..., "sentiment": ...}, ...]
    """
    if not news_list:
        st.warning("분석할 뉴스가 없습니다.")
        return

    # ⏱ timestamp → time 필드로 가공
    df = pd.DataFrame([
        {
            "time": news.get("timestamp"),  # timestamp 필드를 시각화용 time으로 변환
            "score": news.get("sentiment", 0.0)
        }
        for news in news_list if news.get("timestamp")
    ])

    if df.empty:
        st.warning("표시할 뉴스 감정 데이터가 없습니다.")
        return

    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time")

    fig = px.line(df, x="time", y="score", title="🧠 시간대별 뉴스 감정 추이", markers=True)
    fig.update_layout(
        yaxis_title="감정 점수 (-1 ~ +1)",
        xaxis_title="시간",
        xaxis=dict(tickformat="%H:%M\n%m-%d"),
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)
