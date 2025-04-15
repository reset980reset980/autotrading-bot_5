"""
파일명: utils/config_loader.py
📌 목적:
  - 설정값(json/env 파일) 불러오기 및 적용

📦 기능:
  - load_config(): config.json 파일에서 설정값 로드
  - load_env(): .env 파일에서 환경 변수 로드

🧠 작업 프롬프트:
  ▶ "API 키, 경로 등 민감한 설정을 외부에서 로드할 수 있도록 구성하고, 향후 배포 시에도 유연하게 대응할 수 있도록 하라."
"""

import json
import os
from dotenv import load_dotenv

def load_config(path="config.json"):
    """
    📁 config.json 설정값 로드
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} 파일이 존재하지 않습니다.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_env(path=".env"):
    """
    🔐 .env 환경 변수 로드
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} 파일이 존재하지 않습니다.")
    load_dotenv(dotenv_path=path)
