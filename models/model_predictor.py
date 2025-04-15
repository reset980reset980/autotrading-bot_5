"""
파일명: models/model_predictor.py
목적: 학습된 딥러닝 모델을 이용한 전략 예측
기능:
  - 최신 시뮬레이션 또는 실시간 입력 데이터를 받아 전략 예측
  - 0~1 사이 확률값 기반 LONG/SHORT/HOLD 판단
  - 이전에 저장된 모델(.h5)과 스케일러(.pkl) 불러와 사용

전체 흐름도:
  [실시간 입력 or 시뮬레이션 로그]
          ↓
  [utils/data_cleaner.py] → 실시간 입력 전처리
          ↓
  [models/model_predictor.py]
          ↓
  전략 예측: "long", "short", "hold" 중 하나 반환

사용 프롬프트 요약:
  ▶ "학습된 모델을 기반으로 최신 입력값에 대한 전략 방향을 예측하라 (확률 기준 long/short/hold 분기 포함)."
"""
import os
import numpy as np
from tensorflow.keras.models import load_model
from utils.data_cleaner import preprocess_single_entry

# ✅ 모델 경로 (사용자 설정 가능)
MODEL_PATH = "models/lstm_model.h5"

def predict_with_model(entry: dict) -> str:
    """
    딕셔너리 형태의 전략 입력값으로부터 딥러닝 예측 수행
    entry: {
        "rsi": 45.0,
        "macd": -2.1,
        "ema": 27000,
        "tema": 27200,
        "sentiment": 0.2,
        "community_sentiment": 0.1
    }
    """
    if not os.path.exists(MODEL_PATH):
        print("❌ 딥러닝 모델 파일이 존재하지 않습니다.")
        return "hold"

    try:
        model = load_model(MODEL_PATH)
        X = preprocess_single_entry(entry)
        prediction = model.predict(X, verbose=0)
        idx = int(np.argmax(prediction))

        if idx == 0:
            return "long"
        elif idx == 1:
            return "short"
        else:
            return "hold"

    except Exception as e:
        print(f"⚠️ 딥러닝 예측 오류: {e}")
        return "hold"