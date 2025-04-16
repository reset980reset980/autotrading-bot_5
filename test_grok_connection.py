# test_grok_connection.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 GROK_API_KEY 불러오기

API_KEY = os.getenv("GROK_API_KEY")

if not API_KEY:
    print("❌ GROK_API_KEY가 설정되어 있지 않습니다. .env 파일 확인 필요.")
else:
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-3",
        "messages": [
            {"role": "user", "content": "Hello, this is a test request from my system. Please confirm connection."}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ 응답 성공!")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"❌ 연결 오류 발생: {e}")
