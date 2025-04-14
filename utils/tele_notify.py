import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    """
    텔레그램 채널 또는 사용자에게 메시지를 전송합니다.
    환경변수에 TELEGRAM_TOKEN과 TELEGRAM_CHAT_ID가 설정되어 있어야 합니다.
    """
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ 텔레그램 토큰 또는 챗 ID 누락. 메시지 전송 안됨.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print("⚠️ 텔레그램 메시지 전송 실패:", response.text)
    except Exception as e:
        print(f"❌ 텔레그램 오류: {e}")
