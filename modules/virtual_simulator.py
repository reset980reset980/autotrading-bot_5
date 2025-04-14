virtual_balance = 1_000_000  # 초기 시드

def execute_virtual_trade(result: dict):
    global virtual_balance
    signal = result["signal"]
    entry = result["entry_price"]
    tp = result["tp"]
    sl = result["sl"]
    confidence = result.get("confidence", 0)

    # 단순 PnL 계산
    risk_amount = 10_000
    pnl = 0
    if confidence >= 0.5:
        pnl = (tp - entry) / entry * risk_amount if signal == "long" else (entry - sl) / entry * risk_amount
        virtual_balance += pnl
        outcome = "✅ WIN"
    else:
        pnl = (entry - sl) / entry * risk_amount if signal == "long" else (tp - entry) / entry * risk_amount
        virtual_balance -= pnl
        outcome = "❌ LOSS"

    return {
        "mode": "simulator",
        "balance": round(virtual_balance, 2),
        "pnl": round(pnl, 2),
        "result": outcome
    }
