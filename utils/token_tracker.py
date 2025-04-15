# 📁 파일명: utils/token_tracker.py
"""
📌 목적: AI API 호출 시 사용된 토큰 수 및 비용 추적
📌 기능:
  - track_token_usage(): 요청마다 토큰 수 추적
  - get_token_cost(): 모델별 예상 요금 계산
📌 프롬프트 요약:
  ▶ "OpenAI, Grok 등 모델별 토큰 사용량과 비용을 추적하여 시각화하거나 로그에 남기기 위한 모듈을 작성하라."
"""

import os
from datetime import datetime

# 모델별 단가 (USD per 1K tokens)
TOKEN_PRICES = {
    "gpt-4": 0.03,
    "gpt-3.5-turbo": 0.002,
    "grok-3": 0.02,
    "finbert": 0.00  # 로컬 모델 또는 무료 모델
}

USAGE_LOG_PATH = "logs/token_usage_log.txt"

def track_token_usage(model_name: str, tokens_used: int):
    cost = get_token_cost(model_name, tokens_used)

    os.makedirs(os.path.dirname(USAGE_LOG_PATH), exist_ok=True)
    with open(USAGE_LOG_PATH, "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] 모델: {model_name}, 토큰: {tokens_used}, 비용: ${cost:.4f}\n")

    return cost

def get_token_cost(model_name: str, tokens_used: int):
    price_per_1k = TOKEN_PRICES.get(model_name, 0.01)  # 기본값 0.01
    return (tokens_used / 1000) * price_per_1k
