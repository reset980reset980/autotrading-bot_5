# app_dashboard.py
# 📊 AI 기반 암호화폐 자동매매 전략 대시보드 메인 실행 파일
# Streamlit UI 기반 대시보드로 뉴스, 지표, AI 판단, 딥러닝 예측, 전략 실행까지 자동 연동

import streamlit as st
import pandas as pd
import os
import json
from dotenv import load_dotenv
from datetime import datetime

# 🧩 기능 모듈 import
from utils.news_fetcher import fetch_news                  # 뉴스 수집
from utils.sentiment import analyze_news                   # 뉴스 감정 분석
from utils.ohlcv import fetch_ohlcv_data                   # OHLCV 데이터 수집
from utils.indicators import get_indicators                # 기술지표 계산 (RSI, MACD 등)
from utils.grok_bridge import get_grok_response            # Grok API를 통한 전략 분석
from utils.strategy_analyzer import analyze_strategy       # 전략 판단 결과 해석 및 분해
from utils.auto_trader import execute_strategy, save_trade_log  # 시뮬레이터 및 전략 로그 저장
from utils.tele_notify import send_telegram_message        # 텔레그램 알림 기능
from train_model import predict                            # ✅ 딥러닝 기반 전략 예측 함수

# 🌐 .env 파일의 환경변수 로딩
load_dotenv()

# 🔧 Streamlit 기본 페이지 설정
st.set_page_config(page_title="AI 자동매매 전략 대시보드", layout="wide")
st.title("📊 AI 기반 암호화폐 자동매매 전략 대시보드")

# ────────────────────────────────────────────────────────────────
# ✅ Step 1. 최초 실행 시 자동 전략 수집 및 판단 실행
# - 뉴스 수집 → 감정 분석 → 지표 수집 → Grok 응답 → 전략 판단 → 딥러닝 예측
# - 전략 및 판단 내용을 세션 상태에 저장
# ────────────────────────────────────────────────────────────────
if 'strategy' not in st.session_state:
    with st.spinner("📡 전략 분석 중..."):
        news_data = fetch_news()
        sentiment_score = analyze_news(news_data)
        ohlcv = fetch_ohlcv_data()
        indicators = get_indicators(ohlcv)
        grok_response = get_grok_response(indicators, sentiment_score, news_data)
        strategy, details = analyze_strategy(grok_response, indicators, sentiment_score)

        # ✅ 딥러닝 예측값 추가 (논문 기반 전략 강화)
        # 논문 "Deep Learning-based Forecasting of Crypto Price with Technical Indicators"
        # - 주요 기여: RSI, EMA, TEMA, MACD, 감정 점수를 조합한 분류 기반 예측 모델
        ai_prediction = predict([
            indicators["rsi"], indicators["ema"], indicators["tema"],
            indicators["macd"], sentiment_score
        ])
        strategy["ai_prediction"] = ai_prediction

        # ⏺️ 시뮬레이션 로그 저장
        save_trade_log({
            "timestamp": datetime.now().isoformat(),
            **strategy,
            **indicators,
            "sentiment": sentiment_score
        })

        # 💾 상태 저장
        st.session_state.news_data = news_data
        st.session_state.sentiment_score = sentiment_score
        st.session_state.indicators = indicators
        st.session_state.strategy = strategy
        st.session_state.details = details
        st.session_state.grok_response = grok_response

# ────────────────────────────────────────────────────────────────
# ✅ Step 2. 시각화 함수 정의 – 감정 점수 배너
# ────────────────────────────────────────────────────────────────
def display_sentiment(score):
    if score > 0.3:
        st.success(f"🧠 시장 심리: 🟢 긍정적 심리 우세 ({score:.2f})")
    elif score < -0.3:
        st.error(f"🧠 시장 심리: 🔴 부정적 심리 우세 ({score:.2f})")
    else:
        st.warning(f"🧠 시장 심리: ⚪ 중립 또는 혼조 ({score:.2f})")

# ────────────────────────────────────────────────────────────────
# ✅ Step 3. 전략 판단 및 근거 시각화
# ────────────────────────────────────────────────────────────────
def display_strategy_result(strategy, detail):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 🤖 전략 판단 결과")
        signal = strategy["signal"]
        color = {"long": "green", "short": "red", "hold": "gray"}.get(signal, "blue")
        emoji = {"long": "📈", "short": "📉", "hold": "⏸️"}.get(signal, "🤖")
        st.markdown(f"<h2 style='color:{color};'>{emoji} {signal.upper()}</h2>", unsafe_allow_html=True)
        st.text(f"TP: {strategy['tp']}% / SL: {strategy['sl']}%")
        st.markdown(f"🧠 AI 예측 전략: {strategy['ai_prediction']}")

    with col2:
        st.markdown("### 📊 전략 판단 근거 요약")
        st.markdown(f"- RSI: {detail['rsi']:.2f}")
        st.markdown(f"- BB 위치: {detail['bb']}")
        st.markdown(f"- EMA: {detail['ema']:.2f}, TEMA: {detail['tema']:.2f}")
        st.markdown(f"- MACD: {detail['macd']:.2f}")
        st.markdown(f"- 감정 점수: {detail['sentiment']:.2f}")
        st.markdown(f"📌 해석 요약: {detail['summary']}")

# ────────────────────────────────────────────────────────────────
# ✅ Step 4. 뉴스 리스트 + 감정 분석 결과 시각화
# ────────────────────────────────────────────────────────────────
def display_news_list(news_list):
    st.subheader("📰 주요 뉴스 및 감정 결과")
    for news in news_list:
        score = news.get("sentiment", 0)
        icon = "🟢" if score > 0.3 else "🔴" if score < -0.3 else "⚪"
        st.markdown(f"- {icon} [{news['title']}]({news['url']})")

# ────────────────────────────────────────────────────────────────
# ✅ Step 5. 전략 판단 우위 흐름 꺾은선 그래프 시각화
# ────────────────────────────────────────────────────────────────
def display_dominance_chart():
    path = "logs/simulated_trades.json"
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = []
    for row in data[-10:]:  # 최근 10개 기록
        ai_weight = 0.3 + (0.2 if abs(row['sentiment']) > 0.3 else 0)
        tech_weight = 1.0 - ai_weight
        records.append({
            "timestamp": row["timestamp"][-8:],
            "AI 우위": ai_weight,
            "기술 우위": tech_weight
        })
    df = pd.DataFrame(records).set_index("timestamp")
    st.line_chart(df)

# ────────────────────────────────────────────────────────────────
# ✅ Step 6. 텔레그램 메시지 발송 (전략 요약 알림)
# ────────────────────────────────────────────────────────────────
send_telegram_message(f"""
📢 [AI 자동 전략]
🕒 {datetime.now().strftime('%Y-%m-%d %H:%M')}
전략: {st.session_state.strategy['signal'].upper()}
TP: {st.session_state.strategy['tp']}% / SL: {st.session_state.strategy['sl']}%
AI 판단: {st.session_state.strategy['ai_prediction']}
감정: {st.session_state.sentiment_score:.2f}
""")

# ────────────────────────────────────────────────────────────────
# ✅ Step 7. 시각화 순서대로 실행
# ────────────────────────────────────────────────────────────────
display_sentiment(st.session_state.sentiment_score)
display_strategy_result(st.session_state.strategy, st.session_state.details)
st.markdown("---")
display_news_list(st.session_state.news_data)
st.markdown("---")
st.subheader("📈 전략 판단 주체 흐름")
display_dominance_chart()
st.markdown("---")
st.caption("🧠 본 시스템은 자동 실행되며, 수동 조작 및 분석도 병행 가능합니다.")
