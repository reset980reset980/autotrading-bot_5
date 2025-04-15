# 📁 파일명: modules/attention_model.py
# 🎯 목적: Attention 기반 딥러닝 모델로 시계열 가격 흐름 및 감정 점수 예측
# 🔁 전체 흐름도:
#     - 학습: 뉴스 감정 점수 + 기술 지표 + 시세 → 미래 시그널 예측
#     - 예측: 현재 지표 입력 → LONG / SHORT / HOLD 시그널 출력
# 🔧 주요 함수:
#     - train_model(): 과거 데이터를 기반으로 예측 모델 학습
#     - predict_signal(): 현재 지표 기반 시그널 예측
#     - save_model() / load_model(): 모델 저장 및 불러오기
# 💬 프롬프트 요약:
#     ▶ "기술 지표와 감정 데이터를 입력 받아, 딥러닝으로 전략 시그널을 예측하라."

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import os

MODEL_PATH = "models/attention_model.pt"

# 🔹 Attention 기반 간단한 시계열 예측 모델 정의
class AttentionModel(nn.Module):
    def __init__(self, input_size, hidden_size=64):
        super(AttentionModel, self).__init__()
        self.rnn = nn.GRU(input_size, hidden_size, batch_first=True)
        self.attn = nn.Linear(hidden_size, 1)
        self.out = nn.Linear(hidden_size, 3)  # [LONG, SHORT, HOLD]

    def forward(self, x):
        out, _ = self.rnn(x)
        weights = torch.softmax(self.attn(out), dim=1)
        context = torch.sum(weights * out, dim=1)
        return self.out(context)

# 🔸 시그널 인코딩
def encode_signal(signal: str) -> int:
    return {"long": 0, "short": 1, "hold": 2}.get(signal, 2)

def decode_signal(index: int) -> str:
    return ["long", "short", "hold"][index]

# 🔹 모델 학습 함수
def train_model(df: pd.DataFrame):
    model = AttentionModel(input_size=6)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # 입력: [rsi, macd, ema, tema, sentiment, price], 타겟: signal
    X = df[["rsi", "macd", "ema", "tema", "sentiment", "close"]].values
    y = df["signal"].apply(encode_signal).values

    X_tensor = torch.tensor(X, dtype=torch.float32).unsqueeze(1)
    y_tensor = torch.tensor(y, dtype=torch.long)

    for epoch in range(50):
        optimizer.zero_grad()
        output = model(X_tensor)
        loss = criterion(output, y_tensor)
        loss.backward()
        optimizer.step()

    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), MODEL_PATH)

# 🔹 예측 함수
def predict_signal(indicators: dict, sentiment_score: float):
    model = AttentionModel(input_size=6)
    if not os.path.exists(MODEL_PATH):
        return "hold"

    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()

    x = np.array([[indicators["rsi"], indicators["macd"], indicators["ema"],
                   indicators["tema"], sentiment_score, indicators["close"]]])
    x_tensor = torch.tensor(x, dtype=torch.float32).unsqueeze(1)
    with torch.no_grad():
        output = model(x_tensor)
        prediction = torch.argmax(output, dim=1).item()
    return decode_signal(prediction)
