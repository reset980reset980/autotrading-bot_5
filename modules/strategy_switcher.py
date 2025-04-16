# 📁 파일명: modules/strategy_switcher.py
# 🎯 목적: 복수의 전략 결과 중 성능이 우수한 전략을 자동 선택하여 사용
# 🔁 전체 흐름도:
#     - 각 전략 결과(score 포함)를 수집
#     - 성능 점수 기반으로 우선 순위 선택
#     - 상황에 따라 AI 기반 전략, 룰 기반 전략 중 하나를 채택
# 🔧 주요 함수:
#     - switch_strategy(): 전략 결과 비교 후 최적 전략 반환
# 💬 작업 프롬프트 요약:
#     ▶ "여러 전략 중 성능이 가장 높은 전략을 선택하여 매매에 반영하라."

from typing import List, Dict, Any

def switch_strategy(strategies: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    전략 후보 리스트에서 최고 성능 전략을 선택합니다.

    Args:
        strategies (List[Dict]): [{"name": "ai", "score": 0.82, "result": {...}}, ...]

    Returns:
        Dict: 선택된 전략의 결과에 'selected_strategy', 'score'를 포함하여 반환
    """
    if not strategies:
        return {"signal": "hold", "reason": "No strategies provided"}

    try:
        # 점수 높은 순으로 정렬
        sorted_strategies = sorted(strategies, key=lambda x: x.get("score", 0), reverse=True)
        best = sorted_strategies[0]

        return {
            **best.get("result", {}),
            "selected_strategy": best.get("name", "unknown"),
            "score": best.get("score", 0)
        }

    except Exception as e:
        return {
            "signal": "hold",
            "reason": f"Strategy selection failed: {str(e)}"
        }

# ✅ 예시 사용
if __name__ == "__main__":
    sample_strategies = [
        {"name": "AI", "score": 0.83, "result": {"signal": "long", "tp": 1.0, "sl": 0.5}},
        {"name": "Rule", "score": 0.77, "result": {"signal": "short", "tp": 1.2, "sl": 0.6}}
    ]
    final = switch_strategy(sample_strategies)
    print("📌 최종 선택 전략:", final)
