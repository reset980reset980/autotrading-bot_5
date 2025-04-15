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

def execute_bybit_test_trade(symbol: str, side: str, entry_price: float, take_profit: float, stop_loss: float):
    import ccxt
    import os
    from dotenv import load_dotenv

    load_dotenv()
    bybit = ccxt.bybit({
        "apiKey": os.getenv("BYBIT_API_KEY_TESTNET"),
        "secret": os.getenv("BYBIT_SECRET_TESTNET"),
        "enableRateLimit": True,
        "options": {"defaultType": "future"},
    })
    bybit.set_sandbox_mode(True)

    print(f"🛠️ Bybit 테스트넷 주문 실행 중: {side.upper()}")

    # 주문 수량은 최소 단위로 설정 (BTC 기준 0.01)
    amount = 0.01

    try:
        order = bybit.create_order(
            symbol=symbol,
            type="market",
            side=side,
            amount=amount,
            params={
                "takeProfit": round(entry_price * (1 + take_profit / 100), 2) if side == "long" else round(entry_price * (1 - take_profit / 100), 2),
                "stopLoss": round(entry_price * (1 - stop_loss / 100), 2) if side == "long" else round(entry_price * (1 + stop_loss / 100), 2),
            }
        )
        print(f"✅ 테스트넷 주문 성공: {order['id']}")
    except Exception as e:
        print(f"❌ 테스트넷 주문 실패: {e}")
