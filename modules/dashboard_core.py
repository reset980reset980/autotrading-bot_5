# Sample Python module

def example():
    print('This is a sample.')
# 📁 파일명: modules/dashboard_core.py
# 🎯 목적: Streamlit 기반 대시보드의 핵심 기능 관리
# 기능 요약:
#   - 전략 실행 및 감정 분석 결과 시각화
#   - 뉴스 표시 및 전략 요약
#   - 로그 기록 및 텔레그램 전송 포함
# 사용 프롬프트 요약:
#   ▶ "뉴스 + 지표 + 감정 분석 + AI 전략 판단을 통합하여 대시보드에 표시하라."

import streamlit as st
from utils.news_fetcher import fetch_news
from utils.sentiment import analyze_news, get_sentiment_summary
from utils.indicators import get_indicators
from utils.strategy_analyzer import run_strategy, get_strategy_summary
from modules.logger import log_to_file
from modules.telegram_notifier import notify_trade_result


def display_dashboard():
    """
    📊 전체 대시보드 구성 함수
    - 뉴스 수집
    - 전략 실행
    - 감정 분석 결과 및 전략 요약 시각화
    """
    st.set_page_config(page_title="AI 자동매매 대시보드", layout="wide")
    st.title("🤖 AI 자동매매 전략 대시보드")
    st.caption("뉴스 + 지표 + 감정 분석 기반 전략")

    col1, col2 = st.columns([2, 3])

    with col1:
        st.subheader("📰 뉴스 수집")
        if st.button("뉴스 가져오기"):
            news = fetch_news()
            for article in news:
                st.markdown(f"- [{article['title']}]({article['url']})")

        st.subheader("📈 전략 실행")
        if st.button("전략 실행"):
            result = run_strategy()
            st.success(get_strategy_summary(result))

            # 전략 로그 저장
            log_to_file("strategy_log.txt", str(result))

            # 텔레그램 전송 (모의 결과 예시)
            notify_trade_result(result, {
                "result": "N/A",
                "pnl": 0,
                "balance": 0
            })

    with col2:
        st.subheader("💡 감정 분석 및 지표 요약")
        news = fetch_news()
        sentiment_score = analyze_news(news)
        sentiment_text = get_sentiment_summary(sentiment_score)
        st.info(f"🧠 감정 분석 결과: {sentiment_text} (점수: {sentiment_score:.2f})")

        st.markdown("### 기술적 지표")
        indicators = get_indicators("BTC/USDT", timeframe="15m")
        st.json(indicators)


# 단독 실행 시 Streamlit 대시보드 실행
if __name__ == "__main__":
    display_dashboard()
