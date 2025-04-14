# utils/indicators_g.py
import pandas as pd
import numpy as np

def get_indicators(df):
    """
    기술 지표 계산
    :param df: OHLCV 데이터프레임
    :return: 기술 지표 딕셔너리 (시리즈 형태로 반환)
    """
    # RSI 계산
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # EMA 계산
    ema = df['close'].ewm(span=20, adjust=False).mean()

    # TEMA 계산
    ema1 = df['close'].ewm(span=20, adjust=False).mean()
    ema2 = ema1.ewm(span=20, adjust=False).mean()
    ema3 = ema2.ewm(span=20, adjust=False).mean()
    tema = 3 * ema1 - 3 * ema2 + ema3

    # MACD 계산
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2

    # 볼린저 밴드 계산
    rolling_mean = df['close'].rolling(window=20).mean()
    rolling_std = df['close'].rolling(window=20).std()
    bb_upper = rolling_mean + 2 * rolling_std
    bb_lower = rolling_mean - 2 * rolling_std
    bb_status = "상단" if df['close'].iloc[-1] > bb_upper.iloc[-1] else "하단" if df['close'].iloc[-1] < bb_lower.iloc[-1] else "중단"

    # 다이버전스 계산 (간단한 구현)
    price_low = df['close'].rolling(window=14).min()
    rsi_low = rsi.rolling(window=14).min()
    divergence = "강세 다이버전스" if price_low.iloc[-1] < price_low.iloc[-2] and rsi_low.iloc[-1] > rsi_low.iloc[-2] else "없음"

    return {
        "rsi": rsi,  # Pandas Series 반환
        "ema": ema,  # Pandas Series 반환
        "tema": tema,  # Pandas Series 반환
        "macd": macd,  # Pandas Series 반환
        "bb_upper": bb_upper,  # Pandas Series 반환
        "bb_lower": bb_lower,  # Pandas Series 반환
        "bb": bb_status,  # 스칼라 값
        "divergence": divergence  # 스칼라 값
    }