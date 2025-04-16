# 📁 파일명: modules/retrain_scheduler.py
# 🎯 목적: 성능 저하 또는 일정 주기 경과 시 자동으로 모델 재학습을 유도
# 🔁 전체 흐름도:
#     - 마지막 학습 시점과 현재 시점 비교
#     - 성능 저하 감지 여부 확인
#     - 재학습 조건 충족 시 True 반환
# 🔧 주요 함수:
#     - should_retrain(): 재학습 필요 여부 판단
# 💬 작업 프롬프트 요약:
#     ▶ "전략이 일정 기간 또는 성능 저하 시 자동으로 재학습되도록 트리거 로직을 만들어라."

from datetime import datetime
from typing import Optional

def should_retrain(
    last_trained: str,
    current_time: Optional[str] = None,
    performance_drop: bool = False,
    retrain_interval_days: int = 3
) -> bool:
    """
    성능 저하 또는 일정 기간 경과 시 재학습 조건을 판단합니다.

    Args:
        last_trained (str): 마지막 학습 일시 (ISO 형식: "2025-04-10")
        current_time (Optional[str]): 현재 시간 (없을 경우 자동으로 현재시각 적용)
        performance_drop (bool): 성능 저하 여부
        retrain_interval_days (int): 재학습 권장 주기 (기본 3일)

    Returns:
        bool: 재학습 여부 (True이면 재학습 필요)
    """
    try:
        last_dt = datetime.fromisoformat(last_trained)
        curr_dt = datetime.fromisoformat(current_time) if current_time else datetime.now()
        days_passed = (curr_dt - last_dt).days

        return performance_drop or days_passed >= retrain_interval_days

    except Exception as e:
        print(f"❌ 날짜 파싱 실패: {e}")
        return False


# ✅ 예시 사용
if __name__ == "__main__":
    retrain_needed = should_retrain("2025-04-10", "2025-04-14", performance_drop=False)
    print("📆 재학습 트리거 여부:", retrain_needed)
