import streamlit as st
import time
from utils.news_fetcher import fetch_news
from utils.sentiment import analyze_news
from utils.ohlcv import fetch_ohlcv_data
from utils.indicators import calculate_rsi, calculate_bollinger_bands, calculate_atr
from openai import OpenAI
import re

client = OpenAI()

def generate_trading_prompt(news_data, sentiment_result):
    ohlcv = fetch_ohlcv_data("BTC/USDT", interval="15m", limit=100)
    rsi = calculate_rsi(ohlcv)
    upper, lower = calculate_bollinger_bands(ohlcv)
    atr = calculate_atr(ohlcv)
    current_price = ohlcv[-1][4]

    news_summary = "\n".join([f"- {n['title']}" for n in news_data[:3]])

    gpt_prompt = f"""
당신은 금융시장 자동매매 전략가입니다.

[시장 데이터]
- 현재가: {current_price:.2f} USDT
- RSI: {rsi:.2f}
- 볼린저밴드: 상단 {upper:.2f}, 하단 {lower:.2f}
- ATR: {atr:.2f}

[뉴스 감정 요약]
{sentiment_result}

[최근 뉴스 제목]
{news_summary}

위 정보를 종합하여 롱/숏/관망 중 하나를 판단하고, 손절과 익절 범위까지 제안해 주세요.

또한 아래 예시처럼 포지션 분할 전략까지 포함하여 설명해 주세요:
- 예: "30% 손절 후 상황에 따라 유연하게 대처하고, 나머지 70%는 관망하며 대응합니다."
- 또는: "추세가 강한 상승이 예상되어, 50%는 추세에 편승하고 30%는 관망, 20%는 짧은 익절 전략을 사용합니다."
- 단, 퍼센트는 AI가 상황에 따라 유연하게 조절하며 반드시 정해진 수치는 아닙니다.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": gpt_prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content

def parse_ai_decision(ai_text):
    decision_match = re.search(r"(롱|숏|관망)", ai_text)
    sl_match = re.search(r"손절.*?(\d+\.?\d*)", ai_text)
    tp_match = re.search(r"익절.*?(\d+\.?\d*)", ai_text)

    decision = decision_match.group(1) if decision_match else "분석 불가"
    stop_loss = sl_match.group(1) if sl_match else "없음"
    take_profit = tp_match.group(1) if tp_match else "없음"

    return decision, stop_loss, take_profit

# 페이지 설정
st.set_page_config(page_title="AI 자동 선물 매매 시스템", layout="wide")
st.title("🤖 AI 자동 선물 매매 시스템")

# 상태 변수
if "trading_active" not in st.session_state:
    st.session_state.trading_active = False
if "log_messages" not in st.session_state:
    st.session_state.log_messages = []

# 상태 노티스
if st.session_state.trading_active:
    sentiment = st.session_state.get("sentiment_result", "")
    sentiment_str = str(sentiment).lower()
    if "급락" in sentiment_str or "하락" in sentiment_str:
        color = "#ffebee"
        border_color = "#f44336"
        message = "⚠️ 시장 급락이 예상됩니다. 포지션 주의!"
    elif "급등" in sentiment_str or "상승" in sentiment_str:
        color = "#e8f5e9"
        border_color = "#4caf50"
        message = "📈 시장 급등이 예상됩니다. 기회 포착!"
    else:
        color = "#e3f2fd"
        border_color = "#2196f3"
        message = "🤖 <strong>AI가 전략을 분석 중입니다...</strong>"

    st.markdown(f"""
    <div style='padding: 10px; background-color: {color}; border-left: 5px solid {border_color};'>
        {message}
    </div>
    """, unsafe_allow_html=True)

# 상단 버튼
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    if st.button("트레이딩 시작" if not st.session_state.trading_active else "트레이딩 중지"):
        st.session_state.trading_active = not st.session_state.trading_active
        st.session_state.log_messages.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 트레이딩 {'시작' if st.session_state.trading_active else '중지'}")

with col2:
    if st.button("뉴스 수집"):
        st.session_state.news_data = fetch_news()
        st.session_state.sentiment_result = analyze_news(st.session_state.news_data)
        st.session_state.log_messages.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 뉴스 수집 및 감정 분석 완료")

with col3:
    sentiment_display = st.session_state.get("sentiment_result", "분석되지 않음")
    st.markdown(f"**감정 분석 결과:** {sentiment_display}")

# 뉴스 출력
st.subheader("📰 주요 뉴스")
for news in st.session_state.get("news_data", [])[:3]:
    with st.expander(news['title']):
        st.write(news['description'])
        st.markdown(f"[🔗 기사 보기]({news['url']})")

# 전략 분석 결과
st.subheader("📊 AI 전략")
if st.session_state.trading_active:
    try:
        prompt = generate_trading_prompt(
            st.session_state.get("news_data", []),
            st.session_state.get("sentiment_result", "")
        )
        st.session_state.last_ai_text = prompt
        decision, sl, tp = parse_ai_decision(prompt)

        st.markdown(f"### ✅ 판단: **{decision}**")
        st.markdown(f"- 손절 제안: `{sl}` USDT")
        st.markdown(f"- 익절 제안: `{tp}` USDT")
        st.text_area("AI 원문 분석 결과", prompt, height=250)

        st.session_state.log_messages.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 전략 업데이트 완료")
    except Exception as e:
        st.session_state.log_messages.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 전략 생성 중 오류: {str(e)}")

# 로그 출력
st.subheader("📋 로그")
st.text_area("로그", "\n".join(st.session_state.log_messages[-20:]), height=200)
