# 📁 파일명: utils/trade_result_parser.py
# 🎯 목적: 전략 실행 로그에서 수익(profit)을 기준으로 결과(result) 자동 판별 및 보완
# 🔁 전체 흐름도:
#     - profit 기준으로 WIN/LOSS 판별
#     - result 없는 경우 자동 보완
#     - 가공된 로그 반환 or 저장
# 🔧 주요 함수:
#     - parse_trade_result(): 단일 로그 항목 정제
#     - enrich_logs(): 로그 리스트 전체 정제
# 💬 작업 프롬프트 요약:
#     ▶ "로그 파일을 읽어, 누락된 result를 자동 생성하고 분석에 활용 가능하게 정제하라."

from typing import List, Dict

def parse_trade_result(trade: Dict) -> Dict:
    """
    단일 거래 로그에서 result 필드를 생성 또는 보완합니다.

    Args:
        trade (dict): 거래 로그 항목 (profit 포함)

    Returns:
        dict: result 포함된 정제된 로그
    """
    if "result" not in trade:
        profit = trade.get("profit", 0.0)
        if profit > 0:
            trade["result"] = "✅ WIN"
        elif profit < 0:
            trade["result"] = "❌ LOSS"
        else:
            trade["result"] = "⚪ HOLD"
    return trade

def enrich_logs(logs: List[Dict]) -> List[Dict]:
    """
    거래 로그 리스트에서 result 필드를 자동 보완합니다.

    Args:
        logs (List[Dict]): 로그 리스트

    Returns:
        List[Dict]: 정제된 로그 리스트
    """
    return [parse_trade_result(log) for log in logs]


# ✅ 예시 사용
if __name__ == "__main__":
    raw_logs = [
        {"timestamp": "2025-04-14T02:11:59", "signal": "long", "profit": 0.0},
        {"timestamp": "2025-04-14T03:30:00", "signal": "short", "profit": 85.0},
        {"timestamp": "2025-04-14T04:45:00", "signal": "long", "profit": -20.0, "result": "❌ LOSS"}
    ]

    enriched = enrich_logs(raw_logs)
    for log in enriched:
        print(log)
