# 📁 파일명: utils/simulator.py
"""
📌 목적: 가상 시뮬레이션 매매 실행 및 로그 기록
📌 기능:
  - execute_simulated_trade(): 전략 결과 기반 시뮬 매매 처리
  - 수익 계산, 잔고 변화, 승패 판단 등 기록
📌 특징:
  - 단순 손익 계산 로직 적용
  - 기본 잔고: 100만원
📌 작업 프롬프트 요약:
  ▶ "signal, entry_price, TP, SL을 기반으로 시뮬레이션 매매를 실행하고 손익을 계산해 로그 형태로 반환하라."
"""

initial_balance = 1_000_000  # 초기 자산
current_balance = initial_balance  # 실행 중 잔고

def execute_simulated_trade(signal: str, entry_price: float, tp: float, sl: float) -> dict:
    global current_balance

    size = 1  # 가정: 고정 포지션 크기
    result = {}
    
    if signal == "long":
        exit_price = entry_price * (1 + tp / 100)
        pnl = (exit_price - entry_price) * size
    elif signal == "short":
        exit_price = entry_price * (1 - tp / 100)
        pnl = (entry_price - exit_price) * size
    else:
        return {"mode": "simulator", "result": "SKIPPED"}

    # 손익 반영
    current_balance += pnl
    result["mode"] = "simulator"
    result["balance"] = current_balance
    result["pnl"] = pnl
    result["result"] = "✅ WIN" if pnl >= 0 else "❌ LOSS"

    return result
