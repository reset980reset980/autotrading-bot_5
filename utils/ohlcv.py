import requests
import pandas as pd
import time

# 📘 [논문 요약 - systems-12-00498 (2024)]
# "딥러닝 기반 암호화폐 예측 성능 비교" 논문에 따르면,
# OHLCV 데이터와 함께 기술지표(SMA, EMA, TEMA, MACD 등)의 조합이
# 단일 가격 요소보다 예측 정확도가 높다고 분석됨.
# 특히 MACD, EMA, TEMA는 LSTM 및 GRU 계열 모델에서 성능 향상에 기여함.

# 이 모듈은 비트겟이나 바이낸스 등에서 15분봉 기준 OHLCV 데이터를 수집하여
# 후속 지표 계산 및 전략 판단, 딥러닝 입력으로 활용합니다.

def fetch_ohlcv_data(symbol="BTCUSDT", interval="15m", limit=100):
    """
    바이낸스에서 OHLCV 데이터 가져오기
    :param symbol: 거래쌍 (default: BTCUSDT)
    :param interval: 시간 간격 (default: 15분봉)
    :param limit: 데이터 갯수 (default: 100개)
    :return: DataFrame
    """
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}

    for _ in range(3):  # 재시도 로직
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            df = pd.DataFrame(data, columns=[
                "open_time", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "num_trades",
                "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
            ])
            df = df.astype({
                "open": float, "high": float, "low": float,
                "close": float, "volume": float
            })
            return df[["open", "high", "low", "close", "volume"]]
        except Exception as e:
            print(f"[재시도 중] OHLCV 수집 실패: {e}")
            time.sleep(1)
    return pd.DataFrame()  # 실패 시 빈 데이터프레임
