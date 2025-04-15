# Sample Python module

def example():
    print('This is a sample.')
# 📁 파일명: modules/ai_model.py
"""
📌 목적: Grok 또는 OpenAI API 기반 전략 판단 응답 생성
📌 기능:
  - query_grok(prompt: str): 지정된 프롬프트를 Grok API에 전달하고 응답 반환
📌 특징:
  - 모델 이름은 payload 내에서 지정 가능 ("grok-3", "grok-3-latest" 등)
  - 번역은 하지 않고 응답을 그대로 반환하며, 사용자에게는 한글로만 결과 제공
📌 작업 프롬프트 요약:
  ▶ "기술 지표와 감정 점수를 포함한 전략 프롬프트를 받아 Grok 모델로 응답 받고, 해당 응답을 원문 그대로 반환하라."
"""

import os
import requests

GROK_API_KEY = os.getenv("GROK_API_KEY")

def query_grok(prompt: str, model: str = "grok-3"):
    """
    Grok API에 프롬프트 전달 후 응답 반환
    """
    url = "https://api.grok.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"⚠️ Grok 응답 오류: {e}")
        return "HOLD"
