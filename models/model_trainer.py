"""
파일명: models/model_trainer.py
목적: 시뮬레이션 로그 기반 딥러닝 학습용 모델 생성 및 저장
기능:
  - clean_and_label_data()로부터 학습 데이터 불러오기
  - 특성 정규화 및 학습/검증 분리
  - GRU 기반 모델 학습
  - 모델 및 스케일러 저장

전체 흐름도:
  [logs/simulation/simulated_trades.json]
          ↓
  [utils/data_cleaner.py] → clean_and_label_data()
          ↓
  [models/model_trainer.py] → 모델 학습 (GRU 기반)
          ↓
  저장:
    - 모델: models/trained_model.h5
    - 스케일러: models/scaler.pkl

사용 프롬프트 요약:
  ▶ "시뮬레이션 거래 데이터를 기반으로 수익 예측 딥러닝 모델을 학습하고, 추후 전략에 활용할 수 있도록 저장하라."
"""

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import joblib

from utils.data_cleaner import clean_and_label_data

MODEL_PATH = "models/trained_model.h5"
SCALER_PATH = "models/scaler.pkl"

def load_training_data():
    df = clean_and_label_data()
    features = df.drop(columns=["label"])
    labels = df["label"]
    return features, labels

def scale_features(X):
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, SCALER_PATH)
    return X_scaled

def build_gru_model(input_dim):
    model = Sequential()
    model.add(Dense(64, input_dim=input_dim, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_and_save_model():
    print("📊 딥러닝 학습 데이터 준비 중...")
    X, y = load_training_data()
    X_scaled = scale_features(X)
    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    print("🧠 GRU 모델 학습 시작...")
    model = build_gru_model(X_train.shape[1])

    early_stop = EarlyStopping(monitor='val_loss', patience=3)
    model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_val, y_val), callbacks=[early_stop])

    print(f"✅ 모델 저장 완료 → {MODEL_PATH}")
    model.save(MODEL_PATH)

if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    train_and_save_model()
