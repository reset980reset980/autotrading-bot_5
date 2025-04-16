# 📁 파일명: modules/telegram_notifier.py
# 🎯 목적: 매매 실행 결과 또는 시스템 이벤트를 실시간으로 텔레그램에 전송
# 🔄 전체 흐름도:
#     - 전략 실행 후 알림 메시지 구성
#     - 텔레그램 API를 통해 메시지 전송
# 📬 주요 함수:
#     - send_telegram_message(): 텍스트 메시지를 지정 채팅방으로 전송
#     - notify_trade_result(): 매매 전략 및 실행 결과 요약 전송
#     - notify_system_event(): 시스템 오류 또는 이벤트 상황 텔레그램 알림
# 🔐 환경 설정: .env 파일에서 TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID 로 설정
# 🧠 작업 프롬프트 요약:
#     ▶ "매매 발생 시 텔레그램으로 요약 메시지를 전송하라. 간결하고 직관적인 형태로 전달될 것."

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message: str):
    """
    📤 텔레그램으로 단순 텍스트 메시지 전송
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ 텔레그램 설정이 누락되어 전송 불가")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print("❌ 텔레그램 전송 실패:", response.text)
    except Exception as e:
        print("⚠️ 텔레그램 전송 중 예외 발생:", e)


def notify_trade_result(entry: dict, result: dict):
    """
    📣 전략 및 거래 결과를 텔레그램으로 전송
    """
    emoji = "✅" if result.get("result") == "WIN" else "❌" if result.get("result") == "LOSS" else "🔍"
    msg = f"""
<code>📈 전략 실행 결과</code>
{emoji} <b>{entry['signal'].upper()}</b>
🎯 TP: {entry['tp']}% | SL: {entry['sl']}%
📊 RSI: {entry['rsi']} | 심리: {entry['sentiment']:.2f}
📝 요약: {entry.get('summary', '요약 없음')}
💰 수익: {result.get('pnl', 'N/A')} | 잔고: {result.get('balance', 'N/A')}
"""
    send_telegram_message(msg.strip())


def notify_system_event(title: str, detail: str):
    """
    ⚠️ 시스템 에러/알림을 위한 별도 텔레그램 메시지
    """
    msg = f"""
🚨 <b>{title}</b>
<code>{detail}</code>
"""
    send_telegram_message(msg.strip())


# ✅ 단독 실행 예시
if __name__ == "__main__":
    notify_trade_result(
        {
            "signal": "long",
            "tp": 1.2,
            "sl": 0.5,
            "rsi": 27.3,
            "sentiment": 0.42,
            "summary": "RSI 과매도, 감정 긍정"
        },
        {
            "result": "✅ WIN",
            "pnl": 123.45,
            "balance": 1012300.0
        }
    )

    notify_system_event(
        "모델 로드 오류",
        "mse 손실 함수가 정의되지 않아 모델 로딩 실패"
    )
