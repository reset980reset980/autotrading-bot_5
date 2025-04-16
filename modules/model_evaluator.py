# modules/model_evaluator.py

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def evaluate_strategy_performance(predictions, actuals, probs=None):
    """
    전략 판단 결과에 대한 성능 지표를 계산합니다.

    Args:
        predictions (List[int]): 예측된 결과 (예: 1=long, 0=short)
        actuals (List[int]): 실제 결과 (같은 형식)
        probs (List[float], optional): positive 클래스의 확률 (AUC 계산용)

    Returns:
        dict: 정확도, 정밀도, 재현율, F1, AUC 점수 반환
    """
    results = {
        "accuracy": accuracy_score(actuals, predictions),
        "precision": precision_score(actuals, predictions, zero_division=0),
        "recall": recall_score(actuals, predictions, zero_division=0),
        "f1_score": f1_score(actuals, predictions, zero_division=0)
    }

    if probs is not None:
        try:
            results["auc"] = roc_auc_score(actuals, probs)
        except Exception:
            results["auc"] = None
    else:
        results["auc"] = None

    return results
