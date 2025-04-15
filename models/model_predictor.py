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

import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

from utils.data_cleaner import preprocess_single_entry

MODEL_PATH = "models/trained_model.h5"
SCALER_PATH = "models/scaler.pkl"

def predict_strategy(entry: dict) -> str:
    """
    실시간 거래 데이터에 대한 전략 예측
    :param entry: {"rsi": ..., "macd": ..., ...}
    :return: "long" | "short" | "hold"
    """
    # 전처리
    df = preprocess_single_entry(entry)

    if df is None or df.empty:
        return "hold"

    # 스케일링 및 모델 로드
    scaler = joblib.load(SCALER_PATH)
    model = load_model(MODEL_PATH)

    x_input = scaler.transform(df.values)
    prob = model.predict(x_input)[0][0]

    if prob > 0.6:
        return "long"
    elif prob < 0.4:
        return "short"
    else:
        return "hold"
