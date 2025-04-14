# modules/testnet_executor.py

from pybit.unified_trading import HTTP
from modules.config_loader import get_config

def execute_bybit_testnet_trade(result: dict):
    config = get_config()
    
    # Bybit 테스트넷 세션 생성
    session = HTTP(
        api_key=config["bybit"]["api_key"],
        api_secret=config["bybit"]["api_secret"],
        testnet=True,
        recv_window=10000  # 타임스탬프 오류 방지
    )

    direction = "Buy" if result["signal"] == "long" else "Sell"
    qty = result.get("qty", 0.01)

    try:
        response = session.place_order(
            category="linear",
            symbol="BTCUSDT",
            side=direction,
            order_type="Market",
            qty=qty
        )
        return {
            "mode": "bybit_testnet",
            "response": response
        }
    except Exception as e:
        return {
            "mode": "bybit_testnet",
            "error": str(e)
        }
