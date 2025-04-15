# 📁 파일명: utils/ohlcv.py
"""
📌 목적: OHLCV (시가, 고가, 저가, 종가, 거래량) 데이터 수집
📌 기능:
  - fetch_ohlcv_data(symbol, timeframe): 지정 심볼의 OHLCV 데이터 DataFrame 반환
📌 설명:
  - 현재는 샘플 데이터(임의 생성)로 구현되어 있으며, 추후 거래소 API 연동 가능
📌 작업 프롬프트 요약:
  ▶ "주어진 심볼과 타임프레임에 대한 OHLCV 데이터를 반환하는 함수로 구성하되, 초기에는 무작위 데이터 생성 방식으로 제공하라."
"""

import pandas as pd
import random
from datetime import datetime, timedelta

def fetch_ohlcv_data(symbol: str, timeframe: str = "15m", limit: int = 100):
    """
    샘플 OHLCV 데이터를 생성하여 DataFrame 반환
    - 향후 거래소 연동 시 교체 가능
    """
    now = datetime.now()
    data = []
    base_price = 27500

    for i in range(limit):
        time = now - timedelta(minutes=15 * (limit - i))
        open_price = base_price + random.uniform(-100, 100)
        close_price = open_price + random.uniform(-50, 50)
        high_price = max(open_price, close_price) + random.uniform(0, 30)
        low_price = min(open_price, close_price) - random.uniform(0, 30)
        volume = random.uniform(100, 1000)
        data.append([time, open_price, high_price, low_price, close_price, volume])
        base_price = close_price  # 다음 캔들 기준

    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df.set_index("timestamp", inplace=True)
    return df
