# 📁 models/model_predictor.py
# 🎯 시계열 누적 저장 및 딥러닝 예측 함수만 정의

import os
import numpy as np
from tensorflow.keras.models import load_model

SEQUENCE_LENGTH = 10
DATA_SEQUENCE = []

MODEL_PATH = "models/lstm_model.h5"

def update_sequence(entry: dict):
    """
    시계열 데이터 누적 (LSTM 입력용)
    """
    global DATA_SEQUENCE
    features = [
        entry.get("rsi", 50),
        entry.get("macd", 0),
        entry.get("ema", 0),
        entry.get("tema", 0),
        entry.get("sentiment", 0),
    ]
    DATA_SEQUENCE.append(features)
    if len(DATA_SEQUENCE) > SEQUENCE_LENGTH:
        DATA_SEQUENCE.pop(0)

def predict_with_model() -> str:
    """
    누적된 시계열 데이터를 기반으로 전략 예측
    """
    if not os.path.exists(MODEL_PATH):
        print("❌ 모델 파일이 존재하지 않습니다.")
        return "hold"

    if len(DATA_SEQUENCE) < SEQUENCE_LENGTH:
        print("⏳ 시계열 데이터 부족 (예측 보류)")
        return "hold"

    try:
        model = load_model(MODEL_PATH)
        X = np.array([DATA_SEQUENCE], dtype=np.float32)  # (1, 10, 5)
        prediction = model.predict(X, verbose=0)
        idx = int(np.argmax(prediction))
        return ["long", "short", "hold"][idx]
    except Exception as e:
        print(f"⚠️ 예측 오류: {e}")
        return "hold"
