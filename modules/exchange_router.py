from modules.config_loader import get_config
from modules.virtual_simulator import execute_virtual_trade
from modules.testnet_executor import execute_bybit_testnet_trade
from modules.real_executor import execute_bitget_real_trade

def route_trade(result: dict):
    config = get_config()
    mode = config["mode"]
    confidence = result.get("confidence", 0)

    if mode == "sim":
        return execute_virtual_trade(result)
    elif mode == "real":
        return execute_bitget_real_trade(result)
    elif mode == "auto":
        if confidence >= config["real_trade_threshold"]:
            return execute_bitget_real_trade(result)
        elif confidence >= config["testnet_threshold"]:
            return execute_bybit_testnet_trade(result)
        else:
            return execute_virtual_trade(result)
    else:
        return {"error": "Invalid mode in config.json"}
