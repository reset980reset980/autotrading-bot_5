# modules/model_ensemble.py

from collections import Counter

def voting_ensemble(predictions: dict) -> str:
    """
    여러 AI 모델의 판단 결과를 투표 방식으로 통합합니다.

    Args:
        predictions (dict): 모델별 판단 결과
            예: {"GPT": "long", "Grok": "short", "XGBoost": "long"}

    Returns:
        str: 최종 선택된 전략 (예: "long", "short", "hold")
    """
    votes = list(predictions.values())
    vote_counts = Counter(votes)
    most_common = vote_counts.most_common(1)

    if not most_common:
        return "hold"
    return most_common[0][0]
