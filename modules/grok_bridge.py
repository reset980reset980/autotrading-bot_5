"""
파일명: modules/grok_bridge.py
📌 목적:
  - Grok API (xAI 기반)와의 연결을 통해 전략 판단을 위한 AI 응답을 받음
  - API 호출 시 프롬프트를 전달하고 응답을 수신

📦 의존 라이브러리:
  - requests
  - os
  - dotenv (.env에서 GROK_API_KEY 로드)

📤 주요 함수:
  - query_grok(prompt: str, model: str = "grok-3") → str

🔐 프롬프트:
  ▶ "주어진 기술 지표와 감정 점수를 기반으로 LONG/SHORT/HOLD 중 어떤 전략이 적합한지 판단해줘."
"""

import os
import requests
from dotenv import load_dotenv

# .env에서 API 키 로딩
load_dotenv()
GROK_API_KEY = os.getenv("GROK_API_KEY")

# 최신 엔드포인트로 교체됨
GROK_API_URL = "https://api.x.ai/v1/chat/completions"

def query_grok(prompt: str, model: str = "grok-3-beta") -> str:
    """
    Grok API에 전략 판단 프롬프트 전달 → 한국어 응답으로 반환
    """
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI trading assistant. "
                    "Please answer in Korean only. "
                    "Respond concisely and directly with LONG, SHORT, or HOLD decisions."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(GROK_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("⚠️ Grok 호출 실패:", e)
        return "HOLD"
