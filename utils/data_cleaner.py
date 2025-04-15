# 📁 파일명: auto_trader.py
"""
📌 목적: 전체 자동매매 전략 실행 프로세스
📌 기능:
  - 전략 판단(run_strategy)
  - 매매 실행(route_trade)
  - 로그 저장 및 출력
📌 구조:
  - 15분봉 기준으로 1회 전략 실행 (크론탭 or 수동 실행 시)
📌 작업 프롬프트 요약:
  ▶ "전략 판단, 매매 분기, 로그 저장을 모두 포함한 자동매매 실행 루프를 구성하라."
"""

import os
from dotenv import load_dotenv
from datetime import datetime
from utils.strategy_analyzer import run_strategy, get_strategy_summary
from modules.exchange_router import route_trade

load_dotenv()

def main():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n🕒 [{now}] 전략 실행 시작 -----------------------------")

    try:
        # 1. 전략 판단
        strategy_result = run_strategy()
        print("📊 전략 판단 결과:", strategy_result)

        # 2. 매매 실행
        trade_result = route_trade(strategy_result)
        print("🚀 매매 실행 결과:", trade_result)

        # 3. 결과 로그 저장
        with open("logs/strategy_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{now}] 전략: {strategy_result['signal']} | TP: {strategy_result['tp']}% | SL: {strategy_result['sl']}% | RSI: {strategy_result['rsi']} | 감정: {strategy_result.get('sentiment', 0)} | 결과: {trade_result}\n")

    except Exception as e:
        print(f"⚠️ 전략 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
