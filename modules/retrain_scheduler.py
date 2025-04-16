# modules/retrain_scheduler.py

import datetime

def should_retrain(last_trained: str, current_time: str, performance_drop: bool = False, retrain_interval_days: int = 3) -> bool:
    """
    주기적 또는 성능 저하 기반으로 재학습 조건을 판단합니다.

    Args:
        last_trained (str): 마지막 학습 일자 (ISO 8601 형식, 예: "2025-04-10")
        current_time (str): 현재 시간 (ISO 형식, 예: "2025-04-14")
        performance_drop (bool): 전략 성능 저하 여부 (ex. 최근 수익률 급감 등)
        retrain_interval_days (int): 학습 주기 (기본 3일)

    Returns:
        bool: 재학습 여부 판단 결과
    """
    try:
        last_dt = datetime.datetime.fromisoformat(last_trained)
        curr_dt = datetime.datetime.fromisoformat(current_time)
        days_passed = (curr_dt - last_dt).days

        if performance_drop:
            return True
        if days_passed >= retrain_interval_days:
            return True
        return False
    except Exception as e:
        print(f"[재학습 스케줄러 오류] 날짜 파싱 실패: {e}")
        return False
