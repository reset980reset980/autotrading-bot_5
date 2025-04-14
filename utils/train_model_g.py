# utils/train_model_g.py
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import os

MODEL_PATH = "models/lstm_model.h5"

# 데이터 전처리
def preprocess_data(data, sequence_length=10):
    try:
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data)
        
        X, y = [], []
        for i in range(len(scaled_data) - sequence_length):
            X.append(scaled_data[i:i + sequence_length])
            y.append(scaled_data[i + sequence_length, 0])  # 종가를 예측
        
        X, y = np.array(X), np.array(y)
        if len(X) == 0:
            raise ValueError("전처리 후 데이터가 비어 있습니다.")
        return X, y, scaler
    except Exception as e:
        print(f"데이터 전처리 실패: {e}")
        raise

# LSTM 모델 생성
def create_model(input_shape):
    try:
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(50),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        print("LSTM 모델 생성 성공")
        return model
    except Exception as e:
        print(f"모델 생성 실패: {e}")
        raise

# 모델 학습 및 저장
def train_model(data):
    sequence_length = 10
    try:
        print(f"학습 데이터 크기: {len(data)}")
        if len(data) < sequence_length + 1:
            raise ValueError(f"데이터 크기가 너무 작습니다. 최소 {sequence_length + 1}개 필요.")
        
        X, y, scaler = preprocess_data(data, sequence_length)
        
        # 데이터 분할 (80% 학습, 20% 검증)
        train_size = int(len(X) * 0.8)
        if train_size < 1:
            raise ValueError("학습 데이터가 너무 적습니다.")
        X_train, X_val = X[:train_size], X[train_size:]
        y_train, y_val = y[:train_size], y[train_size:]
        
        # 모델 생성
        model = create_model((sequence_length, X.shape[2]))
        
        # 모델 학습
        model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val), verbose=1)
        
        # 모델 저장
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        model.save(MODEL_PATH)
        print(f"모델 저장 완료: {MODEL_PATH}")
        
        return model, scaler
    except Exception as e:
        print(f"모델 학습 실패: {e}")
        raise

# 예측 함수
def predict(features, ohlcv_data=None):
    try:
        # 최신 데이터로 모델 갱신
        if ohlcv_data is not None:
            print(f"OHLCV 데이터 크기: {len(ohlcv_data)}")
            data = ohlcv_data[['open', 'high', 'low', 'close', 'volume']].values
            if len(data) < 10:  # sequence_length보다 작은 경우
                print("OHLCV 데이터가 부족하여 모델 학습 생략")
                try:
                    model = tf.keras.models.load_model(MODEL_PATH)
                    print(f"기존 모델 로드 성공: {MODEL_PATH}")
                except Exception as e:
                    print(f"기존 모델 로드 실패: {e}")
                    return "모델 없음"
            else:
                model, scaler = train_model(data)
        else:
            try:
                model = tf.keras.models.load_model(MODEL_PATH)
                print(f"모델 로드 성공: {MODEL_PATH}")
                data = np.array(features).reshape(-1, 1)
                _, _, scaler = preprocess_data(data)
            except Exception as e:
                print(f"모델 로드 실패: {e}")
                return "모델 없음"

        # 최신 데이터로 예측
        sequence_length = 10
        if len(ohlcv_data) >= sequence_length:
            recent_data = ohlcv_data[['open', 'high', 'low', 'close', 'volume']].values[-sequence_length:]
            scaled_data = scaler.transform(recent_data)
            X = np.array([scaled_data])
            prediction = model.predict(X, verbose=0)
            prediction = scaler.inverse_transform([[prediction[0][0], 0, 0, 0, 0]])[0][0]
            print(f"예측값: {prediction}")
            return prediction
        else:
            print("OHLCV 데이터가 부족하여 예측 불가")
            return "모델 없음"
    except Exception as e:
        print(f"예측 실패: {e}")
        return "모델 없음"

# 실시간 데이터로 모델 갱신 및 예측
def update_and_predict(ohlcv_data, features):
    return predict(features, ohlcv_data)