# 📁 파일명: modules/model_evaluator.py
# 🎯 목적: 전략 판단 결과에 대한 정확도, 정밀도, 재현율, F1, AUC 등 성능 지표 산출
# 🔁 전체 흐름도:
#     - 예측 결과 vs 실제 결과 비교
#     - 분류 성능 지표 계산
#     - 확률 예측(probs) 기반 AUC 제공 (선택)
# 🔧 주요 함수:
#     - evaluate_strategy_performance(): 성능 지표 딕셔너리 반환
# 💬 작업 프롬프트 요약:
#     ▶ "AI 전략 판단의 성능을 수치로 평가하라."

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from typing import List, Optional, Dict

def evaluate_strategy_performance(predictions: List[int], actuals: List[int], probs: Optional[List[float]] = None) -> Dict[str, float]:
    """
    전략 판단 결과에 대한 분류 성능 지표를 계산합니다.

    Args:
        predictions (List[int]): 모델이 예측한 클래스 (0 or 1)
        actuals (List[int]): 실제 클래스 레이블
        probs (Optional[List[float]]): 양성 클래스의 확률 예측 값 (AUC 계산에 필요)

    Returns:
        Dict[str, float]: accuracy, precision, recall, f1_score, auc 포함한 평가 결과
    """
    results = {
        "accuracy": accuracy_score(actuals, predictions),
        "precision": precision_score(actuals, predictions, zero_division=0),
        "recall": recall_score(actuals, predictions, zero_division=0),
        "f1_score": f1_score(actuals, predictions, zero_division=0),
    }

    try:
        results["auc"] = roc_auc_score(actuals, probs) if probs else None
    except Exception:
        results["auc"] = None

    return results


# ✅ 예시 사용
if __name__ == "__main__":
    preds = [1, 0, 1, 1, 0]
    actuals = [1, 0, 0, 1, 0]
    probs = [0.92, 0.15, 0.73, 0.87, 0.22]

    result = evaluate_strategy_performance(preds, actuals, probs)
    print("📊 전략 평가 결과:", result)
