# Sample Python module

def example():
    print('This is a sample.')
# 📁 파일명: utils/logger.py
"""
📌 목적: 시스템 전반에 대한 공통 로그 기록 유틸리티
📌 기능:
  - info(), warn(), error() 함수로 구분된 로그 출력 및 저장
  - 로그 파일: logs/system_log.txt
📌 프롬프트 요약:
  ▶ "자동매매 시스템 전체에서 통합 로그를 기록하고 저장할 수 있는 범용 Logger를 구성하라."
"""

import os
from datetime import datetime

LOG_FILE_PATH = "logs/system_log.txt"

def _write_log(level: str, message: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] [{level.upper()}] {message}"

    print(log_line)  # 콘솔 출력
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")

def info(message: str):
    _write_log("INFO", message)

def warn(message: str):
    _write_log("WARN", message)

def error(message: str):
    _write_log("ERROR", message)
