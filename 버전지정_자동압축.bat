# 사용자 지정 이름 '압축_버전지정_자동.py' 에 맞게 배치 파일 수정
bat_script_final = """
@echo off
chcp 65001 > nul
cd /d D:\\ai_trading_streamlit

echo [🧳] 버전 지정 자동 압축을 시작합니다...
python 압축_버전지정_자동.py

pause
"""

bat_final_path = "/mnt/data/🧳버전지정_자동압축.bat"
with open(bat_final_path, "w", encoding="utf-8") as f:
    f.write(bat_script_final)

bat_final_path
