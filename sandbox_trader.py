# sandbox_trader.py
import time
from datetime import datetime
from utils.strategy_analyzer import run_strategy
from modules.exchange_router import route_trade
import os

LOG_PATH = "logs/sandbox_loop.log"
os.makedirs("logs", exist_ok=True)

def execute_trade_cycle():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n🕒 [{now}] 전략 실행 시작 -----------------------------")

    try:
        # 1. 전략 판단
        strategy_result = run_strategy()
        print("📊 전략 판단 결과:", strategy_result)

        # 2. 매매 실행 조건 분기
        if strategy_result["signal"] == "hold":
            print("⏸️ 전략이 HOLD 상태입니다. 매매 생략.")
            trade_result = {"mode": "simulator", "result": "⏸️ HOLD - No Trade"}
        else:
            trade_result = route_trade(strategy_result)
            print("🚀 매매 실행 결과:", trade_result)

        # 3. 로그 기록
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{now}] 전략: {strategy_result['signal']} | TP: {strategy_result['tp']}% | "
                    f"SL: {strategy_result['sl']}% | RSI: {strategy_result['rsi']} | "
                    f"감정: {strategy_result.get('sentiment', 0)} | 결과: {trade_result}\n")

    except Exception as e:
        print("⚠️ 오류 발생:", e)

    print("⏳ 다음 실행까지 15분 대기...\n")

if __name__ == "__main__":
    print("💤 자동매매 루프 시작 (15분 간격)\n")
    while True:
        execute_trade_cycle()
        time.sleep(900)  # 15분 = 900초
