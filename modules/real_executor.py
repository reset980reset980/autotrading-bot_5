from modules.config_loader import get_config

def execute_bitget_real_trade(result: dict):
    # 실제로는 bitget SDK나 requests를 통해 real API를 실행
    # 여기선 예시로 mock 결과 반환
    return {
        "mode": "bitget_real",
        "status": "MOCK_EXECUTED",
        "signal": result["signal"],
        "price": result["entry_price"]
    }
