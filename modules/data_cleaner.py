# 📁 파일명: modules/data_cleaner.py
# 🎯 목적: 딥러닝 학습용 데이터 품질 정제 및 라벨링
# 기능 요약:
#   - clean_trade_data(): 이상치 제거 및 통일된 형식 정리
#   - label_trade_outcomes(): 수익/손실 라벨링
#   - filter_high_quality_data(): 학습용 고품질 샘플 선별
# 사용 프롬프트 요약:
#   ▶ "거래 데이터를 딥러닝 학습에 적합하도록 정제하고, 성능이 좋은 샘플만 추출하라."

import pandas as pd

def clean_trade_data(raw_data: list) -> pd.DataFrame:
    """
    🧹 거래 데이터 정제
    - 불필요한 항목 제거
    - 수치 변환 및 결측치 보정
    - 딥러닝 학습에 필요한 포맷으로 변환
    """
    df = pd.DataFrame(raw_data)
    df = df.dropna()
    df = df[df["signal"].isin(["long", "short"])]
    df["rsi"] = df["rsi"].astype(float)
    df["sentiment"] = df["sentiment"].astype(float)
    df["profit"] = df["profit"].astype(float)
    return df


def label_trade_outcomes(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    🏷️ 거래 결과 라벨링
    - 수익이 threshold 이상이면 1, 손실이면 0
    """
    df["label"] = (df["profit"] >= threshold).astype(int)
    return df


def filter_high_quality_data(df: pd.DataFrame, min_confidence: float = 0.7) -> pd.DataFrame:
    """
    🔍 고품질 샘플만 필터링 (추후 Attention 학습용)
    - RSI가 과매도/과매수에 가까운 데이터
    - 감정 점수가 강하게 긍/부정인 데이터
    """
    condition = (
        ((df["rsi"] < 30) | (df["rsi"] > 70)) &
        ((df["sentiment"] > 0.4) | (df["sentiment"] < -0.4))
    )
    return df[condition]
