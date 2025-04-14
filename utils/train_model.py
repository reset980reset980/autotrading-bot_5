# utils/train_model.py
# 🧠 딥러닝 기반 전략 예측 모델 로딩 및 예측 함수

import numpy as np
import pandas as pd
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# ✅ 모델과 스케일러 파일 경로
MODEL_PATH = "models/strategy_rf_model.pkl"
SCALER_PATH = "models/strategy_scaler.pkl"

# ✅ 예측 함수 정의
def predict(features: list) -> str:
    """
    🎯 기술지표 및 감정점수를 기반으로 전략 예측

    Parameters:
        features (list): RSI, EMA, TEMA, MACD, Sentiment Score

    Returns:
        str: "long" | "short" | "hold"
    """
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
    except FileNotFoundError:
        print("❗ 예측 모델 또는 스케일러 파일을 찾을 수 없습니다.")
        return "hold"

    X = np.array(features).reshape(1, -1)
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)[0]
    return prediction
