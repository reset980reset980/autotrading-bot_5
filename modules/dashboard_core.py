import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import json


from utils.news_fetcher import fetch_news
from utils.sentiment import analyze_news, get_sentiment_summary
from utils.indicators import get_indicators
from utils.strategy_analyzer import run_strategy, get_strategy_summary

from modules.telegram_notifier import notify_trade_result
from modules.logger import log_trade_result
from modules.streamlit_visualizer import visualize_sentiment_over_time
from modules.visualizer import plot_indicators, plot_hourly_performance
from modules.time_impact_analyzer import analyze_by_hour


def display_dashboard():
    st.set_page_config(page_title="AI 자동매매 대시보드", layout="wide")
    st.title("🤖 AI 자동매매 전략 대시보드")
    st.caption("뉴스 + 감정 분석 + 기술 지표 + 전략 판단 통합")

    col1, col2 = st.columns([2, 3])

    # 👉 왼쪽 패널: 뉴스 & 전략 실행
    with col1:
        st.subheader("📰 실시간 뉴스")
        if st.button("📰 뉴스 수집"):
            news = fetch_news()
            for article in news:
                st.markdown(f"- [{article['title']}]({article['url']})")

        st.subheader("⚙️ 전략 실행")
        if st.button("🚀 전략 실행"):
            result = run_strategy()
            st.success(get_strategy_summary(result))
            # 기존 result에 entry 정보도 같이 넣어줘야 함
            dummy_entry = {
                "signal": result.get("signal", "hold"),
                "tp": result.get("tp", 0),
                "sl": result.get("sl", 0),
                "rsi": result.get("rsi", 50),
                "sentiment": result.get("sentiment_score", 0.0)
            }
            log_trade_result(dummy_entry, result)
            notify_trade_result(result, {
                "result": "N/A",
                "pnl": 0,
                "balance": 0
            })

    # 👉 오른쪽 패널: 감정 분석 + 지표 시각화 + 로그 기반 성능 분석
    with col2:
        st.subheader("💡 감정 분석 요약")
        news = fetch_news()
        sentiment_score = analyze_news(news)
        sentiment_text = get_sentiment_summary(sentiment_score)
        st.info(f"🧠 감정 분석 결과: {sentiment_text} (점수: {sentiment_score:.2f})")

        st.markdown("### 📈 감정 점수 시계열")
        visualize_sentiment_over_time(news)

        st.markdown("### 🧪 기술적 지표 시각화")
        try:
            with open("logs/simulation/simulated_trades_cleaned.json", 'r', encoding='utf-8') as f:
                logs = json.load(f)
            plot_indicators(logs)
        except:
            st.warning("⚠️ 로그 파일이 없어 지표 시각화를 건너뜁니다.")

        st.markdown("### ⏱ 시간대별 전략 성능 분석")
        try:
            summary = analyze_by_hour(logs)
            plot_hourly_performance(summary)
        except:
            st.warning("⚠️ 로그 파일이 없어 전략 성능 분석을 건너뜁니다.")
            
if __name__ == "__main__":
    display_dashboard()
            
