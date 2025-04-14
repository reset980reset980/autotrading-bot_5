# utils/ohlcv_g.py
import requests
import pandas as pd
import time

def fetch_ohlcv_data(symbol="BTCUSDT", interval="15m", limit=500):
    """
    바이낸스에서 OHLCV 데이터 가져오기
    :param symbol: 거래쌍 (default: BTCUSDT)
    :param interval: 시간 간격 (default: 15분봉)
    :param limit: 데이터 갯수 (default: 500개)
    :return: DataFrame
    """
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}

    for _ in range(3):  # 재시도 로직
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
            data = response.json()
            if not data:
                print("OHLCV 데이터가 비어 있습니다.")
                return pd.DataFrame()
            df = pd.DataFrame(data, columns=[
                "open_time", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "num_trades",
                "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
            ])
            df = df.astype({
                "open": float, "high": float, "low": float,
                "close": float, "volume": float
            })
            df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
            df.set_index('open_time', inplace=True)
            print(f"OHLCV 데이터 수집 성공: {len(df)}개")
            return df[["open", "high", "low", "close", "volume"]]
        except Exception as e:
            print(f"[재시도 중] OHLCV 수집 실패: {e}")
            time.sleep(1)
    print("OHLCV 데이터 수집 최종 실패")
    return pd.DataFrame()  # 실패 시 빈 데이터프레임