"""
✅ 자동매매 실행기: auto_trader.py
설명: 뉴스 + 가격 + 지표 + 감정분석 기반 전략 판단 후 텔레그램 알림 전송 + 일일 요약 저장
"""

import os
import time
import traceback
from datetime import datetime

from dotenv import load_dotenv
import pandas as pd

from utils.news_fetcher import fetch_news
from utils.sentiment import analyze_sentiment
from utils.ohlcv import fetch_ohlcv_data as get_ohlcv
from utils.indicators import calculate_rsi, calculate_bollinger_bands
import requests

# ==== 1. 설정 불러오기 ====
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SYMBOL = "BTC/USDT"
INTERVAL = "15m"
LIMIT = 150

# ==== 2. 텔레그램 메시지 전송 ====
def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        r = requests.post(url, data=data)
        print("[텔레그램] 응답:", r.text)
    except Exception as e:
        print("[텔레그램 전송 실패]", e)

# ==== 3. 일일 요약 파일 저장 ====
def save_daily_summary(message):
    folder = "logs/daily_summaries"
    os.makedirs(folder, exist_ok=True)
    filename = datetime.now().strftime("%Y-%m-%d") + ".txt"
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(message)

# ==== 4. 전략 판단 로직 ====
def analyze_strategy():
    try:
        # 1) 가격/지표 수집
        df = get_ohlcv(symbol=SYMBOL, interval=INTERVAL, limit=LIMIT)
        df["RSI"] = calculate_rsi(df["close"])
        df = calculate_bollinger_bands(df)

        # 2) 뉴스 수집 + 감정 분석
        news_list = fetch_news()
        news_summary = ""
        sentiment_score = 0
        count = 0

        for news in news_list:
            sentiment = analyze_sentiment(news['title'])
            sentiment_score += sentiment
            news_summary += f"\n- {news['title']} (감정: {sentiment})"
            count += 1

        avg_sentiment = sentiment_score / max(count, 1)

        # 3) 전략 판단
        last_close = df["close"].iloc[-1]
        last_rsi = df["RSI"].iloc[-1]
        bb_upper = df["BB_upper"].iloc[-1]
        bb_lower = df["BB_lower"].iloc[-1]

        if avg_sentiment > 0.2 and last_rsi < 30 and last_close < bb_lower:
            signal = "🟢 롱 진입 시그널 발생"
        elif avg_sentiment < -0.2 and last_rsi > 70 and last_close > bb_upper:
            signal = "🔴 숏 진입 시그널 발생"
        else:
            signal = "⚪ 관망 유지"

        # 4) 텔레그램 + 요약 저장
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"[{now}]\n전략 판단 결과: {signal}\n\nRSI: {last_rsi:.2f}, 종가: {last_close:.2f}\n뉴스 감정 점수: {avg_sentiment:.2f}\n{news_summary}"

        send_telegram(msg)
        save_daily_summary(msg)

    except Exception as e:
        error_msg = f"❌ 전략 판단 중 오류 발생:\n{traceback.format_exc()}"
        send_telegram(error_msg)
        save_daily_summary(error_msg)

# ==== 5. 실행 ====
if __name__ == "__main__":
    analyze_strategy()
