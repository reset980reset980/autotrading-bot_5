# app_dashboard_g.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import json
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from utils.ohlcv_g import fetch_ohlcv_data
from utils.indicators_g import get_indicators
from utils.news_fetcher_g import fetch_news
from utils.sentiment_g import analyze_news
from utils.grok_bridge_g import get_grok_response
from utils.strategy_analyzer_g import analyze_strategy
from utils.train_model_g import update_and_predict
from utils.auto_trader_g import execute_strategy, send_daily_summary_to_telegram, get_current_position, get_trade_history

st.set_page_config(page_title="AI 트레이딩 대시보드", layout="wide")

# 10초마다 자동 갱신
st_autorefresh(interval=10000, key="datarefresh")

def fetch_ohlcv_data_live():
    df = fetch_ohlcv_data()
    print(f"가져온 OHLCV 데이터 크기: {len(df)}")
    return df

def fetch_news_live():
    news = fetch_news()
    print(f"가져온 뉴스 수: {len(news)}")
    return news

with open("style/news_card_style_g.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.subheader("📈 실시간 차트")
df = fetch_ohlcv_data_live()
if df.empty:
    st.error("OHLCV 데이터를 가져오지 못했습니다.")
    st.stop()

# 캔들스틱 차트 생성
fig = go.Figure()

# 캔들스틱 데이터 추가
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name="OHLC"
))

st.subheader("📊 기술 지표 및 예측")
indicators = get_indicators(df)
news_data = fetch_news_live()
sentiment_score = analyze_news(news_data)
grok_response = get_grok_response(indicators, sentiment_score, news_data)
try:
    strategy_response = json.loads(grok_response["text"])
except json.JSONDecodeError as e:
    st.error(f"JSON 파싱 실패: {e}")
    st.stop()

if "error" in strategy_response:
    st.error(strategy_response["error"])
    st.stop()

strategy, details = analyze_strategy(grok_response["text"], indicators, sentiment_score)

features = [indicators["rsi"].iloc[-1], indicators["ema"].iloc[-1], indicators["tema"].iloc[-1], indicators["macd"].iloc[-1], sentiment_score]
ai_prediction = update_and_predict(df, features)

current_price = df['close'].iloc[-1]
execute_strategy({
    "signal": strategy["signal"],
    "tp": strategy["tp"],
    "sl": strategy["sl"],
    "ai_prediction": ai_prediction,
    **indicators,
    "sentiment_score": sentiment_score
}, current_price)

# 기술 지표 오버레이 추가
fig.add_trace(go.Scatter(
    x=df.index,
    y=indicators["ema"],  # Pandas Series로 전달
    mode='lines',
    name='EMA',
    line=dict(color='blue')
))
fig.add_trace(go.Scatter(
    x=df.index,
    y=indicators["tema"],  # Pandas Series로 전달
    mode='lines',
    name='TEMA',
    line=dict(color='purple')
))

# 볼린저 밴드 추가
fig.add_trace(go.Scatter(
    x=df.index,
    y=indicators["bb_upper"],
    mode='lines',
    name='Bollinger Upper',
    line=dict(color='gray', dash='dash')
))
fig.add_trace(go.Scatter(
    x=df.index,
    y=indicators["bb_lower"],
    mode='lines',
    name='Bollinger Lower',
    line=dict(color='gray', dash='dash')
))

# 매수/매도 시점 표시
trade_history = get_trade_history(limit=10)
buy_signals = []
sell_signals = []
buy_dates = []
sell_dates = []

for trade in trade_history:
    timestamp = pd.to_datetime(trade.get("timestamp"))
    if timestamp not in df.index:
        continue
    if trade["signal"] == "long":
        buy_signals.append(df.loc[timestamp, 'close'])
        buy_dates.append(timestamp)
    elif trade["signal"] == "short":
        sell_signals.append(df.loc[timestamp, 'close'])
        sell_dates.append(timestamp)

fig.add_trace(go.Scatter(
    x=buy_dates,
    y=buy_signals,
    mode='markers',
    name='매수',
    marker=dict(symbol='triangle-up', size=10, color='green')
))
fig.add_trace(go.Scatter(
    x=sell_dates,
    y=sell_signals,
    mode='markers',
    name='매도',
    marker=dict(symbol='triangle-down', size=10, color='red')
))

# 현재 포지션 상태 표시
position = get_current_position(current_price)
if position["status"] != "없음":
    fig.add_shape(
        type="line",
        x0=df.index[0],
        x1=df.index[-1],
        y0=position["entry_price"],
        y1=position["entry_price"],
        line=dict(color="orange", width=2, dash="dash"),
        name="진입 가격"
    )

# 차트 레이아웃 설정
fig.update_layout(
    title="비트코인 15분봉 차트",
    xaxis_title="시간",
    yaxis_title="가격 (USDT)",
    xaxis_rangeslider_visible=False
)

st.plotly_chart(fig)

col1, col2, col3 = st.columns(3)
col1.metric("RSI", f"{indicators['rsi'].iloc[-1]:.2f}")
col1.metric("EMA", f"{indicators['ema'].iloc[-1]:.2f}")
col1.metric("TEMA", f"{indicators['tema'].iloc[-1]:.2f}")
col2.metric("MACD", f"{indicators['macd'].iloc[-1]:.2f}")
col2.metric("볼린저밴드", indicators['bb'])
col2.metric("다이버전스", indicators['divergence'])
col3.metric("감정 점수", f"{sentiment_score:.2f}")
col3.metric("AI 예측", ai_prediction)
col3.metric("AI 토큰 사용량", strategy_response.get("token_usage", 0))

st.markdown("### 📝 AI 분석")
st.markdown(f"""
- **전략 방향**: {strategy_response['signal']}  
- **진입 근거**: {strategy_response['reason']}  
- **손절/익절**: TP {strategy_response['tp']}%, SL {strategy_response['sl']}%  
- **요약**: {strategy_response['summary']}
""")

with open("logs/daily_summaries/2025-04-13.txt", "r", encoding="utf-8") as f:
    summary = f.read()
    balance = float(summary.split("시뮬레이션 잔고: $")[1].split("\n")[0])
st.metric("시뮬레이션 잔고", f"${balance:.2f}")

st.subheader("📉 현재 포지션 상태")
if position["status"] == "없음":
    st.write("현재 포지션: 없음")
else:
    st.write(f"""
    - **포지션**: {position['status']}  
    - **진입 가격**: ${position['entry_price']:.2f}  
    - **현재 수익**: ${position['profit']:.2f}
    """)

st.subheader("📜 최근 거래 내역")
if trade_history:
    trade_df = pd.DataFrame(trade_history)
    trade_df = trade_df[["timestamp", "signal", "profit", "rsi", "sentiment_score"]]
    trade_df.columns = ["시간", "전략", "수익($)", "RSI", "감정 점수"]
    st.dataframe(trade_df)
else:
    st.write("거래 내역이 없습니다.")

st.subheader("📰 주요 뉴스 (롤링)")
if "news_index" not in st.session_state:
    st.session_state.news_index = 0

if len(news_data) < 3:
    st.warning("뉴스가 충분하지 않습니다. 최소 3개의 뉴스가 필요합니다.")
    selected_news = news_data
else:
    selected_news = random.sample(news_data, 3)

cols = st.columns(3)
for idx, news in enumerate(selected_news):
    score = news.get("sentiment_score", 0)
    sentiment_class = "positive" if score > 0.3 else "negative" if score < -0.3 else "neutral"
    html = f"""
    <div class="news-card {sentiment_class}">
        <a href="{news['url']}" target="_blank">{news['title']}</a><br>
        <small>{news['source']}</small>
    </div>
    """
    cols[idx].markdown(html, unsafe_allow_html=True)

st.session_state.news_index += 1
if st.session_state.news_index % 10 == 0:
    st.experimental_rerun()