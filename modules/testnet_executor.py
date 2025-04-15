# 📁 파일명: modules/testnet_executor.py
"""
📌 목적: Bybit 테스트넷에 거래 요청을 보내는 실행 모듈
📌 기능:
  - execute_bybit_testnet_trade(): 시그널에 따라 테스트 거래 실행
📌 특징:
  - pybit 사용
  - .env의 BYBIT_API_KEY_TEST, BYBIT_API_SECRET_TEST 활용
📌 작업 프롬프트 요약:
  ▶ "매수/매도 시그널을 받아 Bybit 테스트넷에 시장가 거래를 실행하는 함수를 구성하라."
"""

import os
from pybit.unified_trading import HTTP
from dotenv import load_dotenv

load_dotenv()

# ✅ 테스트넷 전용 API 키
API_KEY = os.getenv("BYBIT_API_KEY_TEST")
API_SECRET = os.getenv("BYBIT_API_SECRET_TEST")

session = HTTP(
    testnet=True,
    api_key=API_KEY,
    api_secret=API_SECRET
)

def execute_bybit_testnet_trade(signal: str, entry_price: float, tp: float, sl: float):
    """
    Bybit 테스트넷에서 시장가 주문 실행
    """
    symbol = "BTCUSDT"
    qty = 0.01
    side = "Buy" if signal == "long" else "Sell"

    try:
        response = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            order_type="Market",
            qty=qty
        )
        return {"mode": "bybit_testnet", "response": response}
    except Exception as e:
        return {"mode": "bybit_testnet", "error": str(e)}
