# 📁 파일명: utils/indicators.py
"""
📌 목적: 암호화폐 기술적 지표 계산 (RSI, MACD, 볼린저밴드 등)
📌 기능:
  - get_indicators(symbol, timeframe): 심볼과 타임프레임에 대한 주요 기술적 지표 계산
  - detect_rsi_divergence(df): 시가/종가 기반 RSI 다이버전스 판단
📌 포함 지표:
  - RSI (상대강도지수, 기준: 20/80)
  - EMA / TEMA
  - MACD
  - 볼린저 밴드 상단/하단 여부
  - RSI 다이버전스 (강세/약세/없음)
📌 작업 프롬프트 요약:
  ▶ "캔들 데이터를 받아 RSI, MACD, EMA, TEMA, 볼린저 밴드를 계산하고, 시가/종가 기반 RSI 다이버전스 여부까지 판단하라."
"""

import numpy as np
import pandas as pd
from utils.ohlcv import fetch_ohlcv_data

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / (loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_ema(series, period=14):
    return series.ewm(span=period, adjust=False).mean()

def calculate_tema(series, period=14):
    ema1 = calculate_ema(series, period)
    ema2 = calculate_ema(ema1, period)
    ema3 = calculate_ema(ema2, period)
    return 3 * (ema1 - ema2) + ema3

def calculate_macd(series, fast=12, slow=26):
    ema_fast = calculate_ema(series, fast)
    ema_slow = calculate_ema(series, slow)
    return ema_fast - ema_slow

def detect_rsi_divergence(df: pd.DataFrame) -> str:
    """
    시가/종가 기준 RSI 다이버전스 판단
    - 강세: 종가 저점 ↓, RSI 저점 ↑
    - 약세: 종가 고점 ↑, RSI 고점 ↓
    """
    close = df["close"]
    open_ = df["open"]
    rsi = calculate_rsi(close)

    if len(df) < 30:
        return "데이터 부족"

    # 강세 다이버전스 (최근 저점 ↓ / RSI 저점 ↑)
    recent_close_low = close.rolling(14).min().iloc[-1]
    prev_close_low = close.rolling(14).min().iloc[-2]

    recent_rsi_low = rsi.rolling(14).min().iloc[-1]
    prev_rsi_low = rsi.rolling(14).min().iloc[-2]

    if recent_close_low < prev_close_low and recent_rsi_low > prev_rsi_low:
        return "강세 다이버전스"

    # 약세 다이버전스 (최근 고점 ↑ / RSI 고점 ↓)
    recent_close_high = close.rolling(14).max().iloc[-1]
    prev_close_high = close.rolling(14).max().iloc[-2]

    recent_rsi_high = rsi.rolling(14).max().iloc[-1]
    prev_rsi_high = rsi.rolling(14).max().iloc[-2]

    if recent_close_high > prev_close_high and recent_rsi_high < prev_rsi_high:
        return "약세 다이버전스"

    return "없음"

def get_indicators(symbol: str, timeframe: str = "15m") -> dict:
    """
    ✅ 전략 판단용 기술적 지표 + 다이버전스 포함
    """
    df = fetch_ohlcv_data(symbol, timeframe)
    if df is None or df.empty:
        return {}

    close = df["close"]

    rsi = calculate_rsi(close).iloc[-1]
    ema = calculate_ema(close).iloc[-1]
    tema = calculate_tema(close).iloc[-1]
    macd = calculate_macd(close).iloc[-1]

    upper_bb = close.rolling(window=20).mean() + 2 * close.rolling(window=20).std()
    lower_bb = close.rolling(window=20).mean() - 2 * close.rolling(window=20).std()

    bb_location = "상단" if close.iloc[-1] >= upper_bb.iloc[-1] else \
                  "하단" if close.iloc[-1] <= lower_bb.iloc[-1] else "중앙"

    divergence = detect_rsi_divergence(df)

    return {
        "rsi": round(rsi, 2),
        "ema": round(ema, 2),
        "tema": round(tema, 2),
        "macd": round(macd, 2),
        "bb": bb_location,
        "divergence": divergence,
        "close": close.iloc[-1]
    }
