# 📁 파일명: utils/data_cleaner.py
# 🎯 목적: 시뮬레이션 및 실시간 전략 판단을 위한 데이터 전처리
# 🔄 전체 흐름도:
#     - JSON 로그 또는 실시간 딕셔너리 데이터를 받아
#     - 정규화 및 시계열 전처리를 통해 모델 입력 형태로 변환
# 📚 주요 함수:
#     - preprocess_single_entry(): 단일 전략 데이터를 딥러닝 입력 형식으로 변환
# 💬 작업 프롬프트 요약:
#     ▶ "전략 판단에 필요한 입력값을 LSTM 모델에 적합한 형식으로 정제하라."

import numpy as np

# ✅ 사용할 피처 목록 (딥러닝 입력용)
FEATURES = ["rsi", "macd", "ema", "tema", "sentiment", "community_sentiment"]

def preprocess_single_entry(entry: dict) -> np.ndarray:
    """
    단일 전략 데이터를 받아서 (1, seq_len, feature) 형태로 변환
    딕셔너리 형태 입력:
        {
            "rsi": 45.0,
            "macd": -2.1,
            "ema": 27000,
            "tema": 27200,
            "sentiment": 0.2,
            "community_sentiment": 0.1
        }
    출력:
        np.array shape = (1, 10, 6)
    """
    try:
        # 1개 샘플을 10번 복제하여 시계열 입력처럼 만듦
        row = [float(entry.get(k, 0)) for k in FEATURES]
        series = [row for _ in range(10)]  # 시계열 길이 = 10
        return np.array([series])  # shape: (1, 10, 6)
    except Exception as e:
        print(f"⚠️ 전처리 오류: {e}")
        return np.zeros((1, 10, len(FEATURES)))

# ✅ 예시 실행용 테스트
if __name__ == "__main__":
    test_entry = {
        "rsi": 34.1,
        "macd": 1.9,
        "ema": 27500,
        "tema": 27300,
        "sentiment": -0.4,
        "community_sentiment": -0.3
    }
    result = preprocess_single_entry(test_entry)
    print(result.shape)  # (1, 10, 6)
    print(result)
