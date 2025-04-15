# 📁 파일명: utils/telegram_notifier.py
"""
📌 목적: 매매 결과, 전략 판단 결과, 시스템 로그 등을 텔레그램으로 실시간 전송
📌 기능:
  - send_message(): 메시지를 지정된 텔레그램 채팅방으로 전송
📌 프롬프트 요약:
  ▶ "거래 결과 또는 전략 분석 내용을 텔레그램으로 실시간 전달할 수 있는 함수 구성, .env에 BOT_TOKEN과 CHAT_ID가 저장되어 있다고 가정함."
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_message(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram 설정값 누락")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"❌ 텔레그램 전송 실패: {response.text}")
    except Exception as e:
        print(f"❌ 텔레그램 통신 오류: {e}")
