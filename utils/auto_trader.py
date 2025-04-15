# utils/auto_trader.py
import json
import os
from datetime import datetime
import pandas as pd

SIMULATION_LOG_PATH = "simulated_trades.json"
DAILY_SUMMARY_PATH = "logs/daily_summaries"
INITIAL_BALANCE = 10000

def load_trade_log():
    if not os.path.exists(SIMULATION_LOG_PATH):
        return []
    with open(SIMULATION_LOG_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except (json.JSONDecodeError, ValueError):
            print("거래 로그 파일이 손상되었습니다. 새 로그 파일을 생성합니다.")
            return []

# 기존 전략 판단
strategy_result = run_strategy()
print("📊 전략 판단 결과:", strategy_result)


# ✅ 여기에 자동 분기 매매 실행 추가
from modules.exchange_router import route_trade
trade_result = route_trade(strategy_result)
print("🚀 매매 실행 결과:", trade_result)

# 이후 기존의 로그 저장 등 유지
log_result(trade_result)


def simulate_trade(signal: str, price: float, tp: float, sl: float):
    if signal == "long":
        profit = price * (tp / 100) - price * (sl / 100)
    else:  # short
        profit = price * (sl / 100) - price * (tp / 100)
    return profit

def save_trade_log(entry: dict):
    # JSON 직렬화를 위해 Series 객체가 포함되어 있는지 확인하고 변환
    for key, value in entry.items():
        if isinstance(value, pd.Series):
            entry[key] = value.iloc[-1] if not value.empty else 0
    entry["timestamp"] = datetime.now().isoformat()
    
    logs = load_trade_log()
    logs.append(entry)
    logs = logs[-1000:]  # 최근 1000개만 유지
    with open(SIMULATION_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

def save_daily_summary(entry: dict):
    os.makedirs(DAILY_SUMMARY_PATH, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    summary_path = os.path.join(DAILY_SUMMARY_PATH, f"{today}.txt")
    
    logs = load_trade_log()
    balance = INITIAL_BALANCE + sum(trade["profit"] for trade in logs)
    
    with open(summary_path, "a", encoding="utf-8") as f:
        f.write(f"[{entry['timestamp']}] {entry['signal']} - 수익: ${entry['profit']:.2f}\n")
        f.write(f"시뮬레이션 잔고: ${balance:.2f}\n")

def send_daily_summary_to_telegram():
    today = datetime.now().strftime("%Y-%m-%d")
    summary_path = os.path.join(DAILY_SUMMARY_PATH, f"{today}.txt")
    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            summary = f.read()
        print(f"텔레그램으로 전송: {summary}")
    else:
        print("오늘의 요약이 없습니다.")

def execute_strategy(entry: dict, price: float):
    profit = simulate_trade(entry["signal"], price, entry["tp"], entry["sl"])
    entry["profit"] = profit
    save_trade_log(entry)
    save_daily_summary(entry)
    
    msg = f"""
🔔 새로운 거래 실행
- 전략: {entry['signal']}
- 수익: ${profit:.2f}
- RSI: {entry['rsi']:.2f}
- 감정 점수: {entry['sentiment_score']:.2f}
"""
    print(msg)

def get_current_position(current_price: float):
    logs = load_trade_log()
    if not logs:
        return {"status": "없음", "entry_price": 0, "profit": 0}
    
    last_trade = logs[-1]
    if last_trade["signal"] in ["long", "short"]:
        profit = (current_price - last_trade["ai_prediction"]) if last_trade["signal"] == "long" else (last_trade["ai_prediction"] - current_price)
        return {
            "status": last_trade["signal"],
            "entry_price": last_trade["ai_prediction"],
            "profit": profit
        }
    return {"status": "없음", "entry_price": 0, "profit": 0}

def get_trade_history(limit: int = 10):
    logs = load_trade_log()
    return logs[-limit:]