from modules.exchange_router import route_trade

if __name__ == "__main__":
    sample_strategy = {
        "signal": "long",
        "entry_price": 65000,
        "tp": 66500,
        "sl": 64500,
        "confidence": 0.82,
        "qty": 0.01
    }

    result = route_trade(sample_strategy)
    print("\n🧪 [TEST RESULT]")
    print(result)
