# 📁 파일명: modules/strategy_flow_chart.py
# 🎯 목적: 전략 판단 결과를 시각적인 흐름도로 표시하여 사용자 이해를 돕는다.
# 📦 의존성: matplotlib
# 📚 주요 함수:
#     - draw_strategy_flow(): RSI, MACD, 감정 점수 등 기반 판단 흐름 표시
# 💬 프롬프트 요약:
#     ▶ "AI 전략 결과를 기반으로 한 시각적 전략 흐름도 그래프를 그려라."

import matplotlib.pyplot as plt
from matplotlib import rcParams

# ✅ Windows 기준 나눔고딕 또는 맑은 고딕 적용
plt.rcParams['font.family'] = 'Malgun Gothic'  # 또는 'NanumGothic'
rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

def draw_strategy_flow(signal: str, indicators: dict):
    """
    전략 흐름도 시각화 함수

    Parameters:
        signal (str): 'long', 'short', 'hold' 중 하나
        indicators (dict): rsi, macd, sentiment, bb 등 포함된 딕셔너리
    """

    # 흐름 단계 및 조건 요약
    stages = [
        "RSI 분석",
        "MACD 분석",
        "감정 분석",
        "BB 위치 분석",
        "AI 전략 판단"
    ]
    
    reasons = [
        f"RSI: {indicators.get('rsi', '-')}",
        f"MACD: {indicators.get('macd', '-')}",
        f"Sentiment: {indicators.get('sentiment', '-')}",
        f"BB 위치: {indicators.get('bb', '-')}",
        f"결과: {signal.upper()}"
    ]
    
    colors = {
        "long": "green",
        "short": "red",
        "hold": "gray"
    }

    fig, ax = plt.subplots(figsize=(8, 5))
    y = list(range(len(stages)))[::-1]

    for i, (stage, reason) in enumerate(zip(stages, reasons)):
        ax.plot([0, 1], [y[i], y[i]], color='black')
        ax.text(0, y[i], stage, ha='right', va='center', fontsize=10, fontweight='bold')
        ax.text(1, y[i], reason, ha='left', va='center', fontsize=10)

    # 최종 전략 강조
    ax.scatter([1.2], [y[-1]], s=150, color=colors.get(signal, 'gray'), label=f"전략: {signal.upper()}")
    ax.legend(loc='upper center')
    
    ax.axis('off')
    plt.title("🧭 전략 판단 흐름도", fontsize=13)
    plt.tight_layout()
    plt.show()
