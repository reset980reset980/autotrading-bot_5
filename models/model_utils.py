"""
파일명: models/model_utils.py
목적: 딥러닝 모델 관련 유틸리티 함수 정의
기능:
  - 모델 저장 및 로드
  - 예측 결과에 따른 신호 변환
  - 확장된 판단 방식 (threshold 기반 전략 분기 등)

전체 흐름도:
  [모델 결과 또는 외부 입력]
          ↓
  [score_to_signal()] 등으로 판단 기준 전환
          ↓
  전략 결과: "long", "short", "hold"

사용 프롬프트 요약:
  ▶ "딥러닝 예측 결과를 기반으로 신호(long/short/hold)를 해석하고, 로딩 및 저장 유틸리티를 제공하라."
"""

import joblib
import numpy as np
from tensorflow.keras.models import load_model, save_model

MODEL_PATH = "models/trained_model.h5"
SCALER_PATH = "models/scaler.pkl"

def load_scaler():
    return joblib.load(SCALER_PATH)

def load_trained_model():
    return load_model(MODEL_PATH)

def save_trained_model(model):
    save_model(model, MODEL_PATH)

def score_to_signal(score: float, threshold_long=0.6, threshold_short=0.4) -> str:
    """
    예측 점수 → 전략 신호 변환
    """
    if score > threshold_long:
        return "long"
    elif score < threshold_short:
        return "short"
    else:
        return "hold"
