# 📁 파일명: modules/exchange_router.py
"""
📌 목적: 전략에 따라 해당 거래 실행 경로 분기 (실거래소 or 시뮬레이터)
📌 기능:
  - route_trade(strategy_result): 전략 결과에 따라 시뮬 or 거래소 실행
📌 구조:
  - signal이 hold일 경우 아무 실행 없이 스킵
  - config.json 설정에 따라 시뮬레이터, 테스트넷, 실매매 분기 처리
📌 작업 프롬프트 요약:
  ▶ "전략 판단 결과를 받아서 실거래소 또는 시뮬레이터 중 어디서 실행할지를 자동 분기 처리하는 모듈을 구성하라."
"""

import json
import os
from modules.testnet_executor import execute_bybit_test_trade  # ✅ 존재하는 함수
from utils.simulator import execute_simulated_trade

def route_trade(strategy_result: dict):
    """
    전략 결과에 따라 실제 거래 또는 시뮬레이션 분기 실행
    """
    signal = strategy_result.get("signal", "hold")
    if signal == "hold":
        print("⏸️ 전략이 HOLD 상태입니다. 매매 생략.")
        return {"mode": "hold", "result": "No action"}

    entry_price = strategy_result.get("entry_price", 27500)
    tp = strategy_result.get("tp", 1.0)
    sl = strategy_result.get("sl", 0.5)

    config_path = "config.json"
    if not os.path.exists(config_path):
        print("⚠️ config.json 파일이 없습니다. 기본값: simulator")
        return execute_simulated_trade(signal, entry_price, tp, sl)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    mode = config.get("trade_mode", "simulator")

    if mode == "simulator":
        return execute_simulated_trade(signal, entry_price, tp, sl)
    elif mode == "bybit_testnet":
        return execute_bybit_test_trade(signal, entry_price, tp, sl)
    else:
        print(f"⚠️ 알 수 없는 거래 모드: {mode}")
        return {"mode": "error", "result": "Unknown mode"}
