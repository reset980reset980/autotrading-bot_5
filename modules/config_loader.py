# 📁 파일명: modules/config_loader.py
# 🎯 목적: config.json 및 .env 등 설정 파일 불러오기 전용
# 기능 요약:
#   - load_config(): config.json 파일 불러오기
#   - load_env(): .env 파일에서 환경 변수 불러오기
# 사용 프롬프트 요약:
#   ▶ "자동매매에 필요한 설정을 config.json 및 .env 파일로 분리 관리하고, 유연하게 로드하라."

import json
import os
from dotenv import load_dotenv

def load_config(path: str = "config.json") -> dict:
    """
    ⚙️ config.json 파일 로딩
    - 기본 설정 (레버리지, 심볼, 지표 등)
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"⚠️ 설정 파일 로딩 실패: {e}")
        return {}

def load_env(env_path: str = ".env"):
    """
    🔐 .env 파일에서 API 키, 비밀키, 토큰 등 불러오기
    - 실행 시 자동 적용됨
    """
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        print("⚠️ .env 파일이 존재하지 않습니다.")
