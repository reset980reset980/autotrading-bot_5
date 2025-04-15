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

def switch_strategy(strategies: list) -> dict:
    """
    전략 후보 리스트에서 최고 성능 전략을 선택 (score 필드 기반)
    :param strategies: [{"name": "ai", "score": 0.82, "result": {...}}, ...]
    :return: 선택된 전략의 result 딕셔너리
    """
    if not strategies:
        return {"signal": "hold", "reason": "No strategies provided"}

    # 점수 높은 순 정렬
    sorted_strategies = sorted(strategies, key=lambda x: x["score"], reverse=True)
    best = sorted_strategies[0]

    return {
        **best["result"],
        "selected_strategy": best["name"],
        "score": best["score"]
    }

# ✅ 예시 사용
if __name__ == "__main__":
    sample_strategies = [
        {"name": "AI", "score": 0.83, "result": {"signal": "long", "tp": 1.0, "sl": 0.5}},
        {"name": "Rule", "score": 0.77, "result": {"signal": "short", "tp": 1.2, "sl": 0.6}}
    ]
    final = switch_strategy(sample_strategies)
    print("📌 최종 선택 전략:", final)
