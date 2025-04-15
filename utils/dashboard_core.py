# 📁 파일명: utils/dashboard_core.py
"""
📌 목적: Streamlit 대시보드에서 전략 결과, 감정 분석, 뉴스 등을 시각적으로 출력하기 위한 공통 함수 모듈
📌 기능:
  - display_strategy_result(): 전략 판단 결과를 시각적으로 표시
  - display_sentiment_banner(): 감정 점수를 배너 형태로 강조
  - display_news_table(): 수집된 뉴스 리스트 시각화
📌 프롬프트 요약:
  ▶ "Streamlit에서 전략 판단 결과와 감정 분석, 뉴스 정보를 시각적으로 효과적으로 표현할 수 있는 컴포넌트 기반 함수들을 구성하라."
"""

import streamlit as st

def display_strategy_result(result: dict):
    signal = result.get("signal", "hold")
    signal_text = {
        "long": "📈 LONG (상승 진입)",
        "short": "📉 SHORT (하락 진입)",
        "hold": "⏸️ HOLD (관망)"
    }.get(signal, "❓")

    color = {
        "long": "lightgreen",
        "short": "#ffb3b3",
        "hold": "lightgray"
    }.get(signal, "white")

    st.markdown(f"""
    <div style="padding:1rem; background-color:{color}; border-radius:1rem;">
        <h4>{signal_text}</h4>
        <p>📌 전략 요약: {result.get('summary', 'N/A')}</p>
        <ul>
            <li>🎯 TP: {result.get('tp', 0)}%</li>
            <li>🛡 SL: {result.get('sl', 0)}%</li>
            <li>📊 RSI: {result.get('rsi')}</li>
            <li>🧠 감정 점수: {result.get('sentiment')}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def display_sentiment_banner(score: float):
    if score > 0.3:
        msg = "📈 긍정적 심리 우세 - 상승 가능성"
        color = "#d4fcd4"
    elif score < -0.3:
        msg = "📉 부정적 심리 우세 - 하락 가능성"
        color = "#fcd4d4"
    else:
        msg = "🔍 혼조 또는 중립 심리"
        color = "#f4f4f4"

    st.markdown(f"""
    <div style="padding:0.5rem; background-color:{color}; border-left:5px solid gray;">
        <strong>{msg}</strong>
    </div>
    """, unsafe_allow_html=True)

def display_news_table(news_list: list):
    for news in news_list:
        st.markdown(f"""
        <div style="border-bottom:1px solid #ccc; padding:0.3rem 0;">
            <a href="{news.get('url')}" target="_blank">
                <strong>{news.get('title')}</strong>
            </a>
            <br><small>📰 {news.get('source')}</small>
        </div>
        """, unsafe_allow_html=True)
