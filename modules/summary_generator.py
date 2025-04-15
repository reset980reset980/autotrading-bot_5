# 📁 파일명: modules/summary_generator.py
# 🎯 목적: 일일 거래 요약 및 성과 기록을 생성하고 저장
# 기능 요약:
#   - save_daily_summary(): 시뮬레이션 및 실거래 결과 요약 저장
#   - get_today_summary(): 오늘자 요약 내용을 조회
# 사용 프롬프트 요약:
#   ▶ "매매 결과를 일별로 정리해 사용자에게 보기 쉽게 제공하라."

import os
from datetime import datetime

# 로그 저장 경로
DAILY_SUMMARY_PATH = "logs/daily_summaries"
os.makedirs(DAILY_SUMMARY_PATH, exist_ok=True)

def save_daily_summary(entry: dict):
    """
    📄 일일 전략 및 수익 요약을 로그 파일에 저장
    - entry: dict 형식의 전략 + 수익 정보
    """
    today = datetime.now().strftime("%Y-%m-%d")
    summary_path = os.path.join(DAILY_SUMMARY_PATH, f"{today}.txt")
    summary = f"""
[{entry.get("timestamp", "알 수 없음")}]
전략: {entry['signal'].upper()} / 수익: ${entry['profit']:.2f}
RSI: {entry['rsi']:.2f} / 감정: {entry['sentiment']:.2f}
📋 요약: {entry['summary']}
잔고: ${entry.get("balance", 0):,.2f}
"""
    with open(summary_path, "a", encoding="utf-8") as f:
        f.write(summary + "\n")


def get_today_summary() -> str:
    """
    📤 오늘 날짜 기준 일일 요약 로그 조회
    - 반환값: 문자열 형태의 로그 요약
    """
    today = datetime.now().strftime("%Y-%m-%d")
    summary_path = os.path.join(DAILY_SUMMARY_PATH, f"{today}.txt")
    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "📭 오늘의 전략 요약이 아직 없습니다."
