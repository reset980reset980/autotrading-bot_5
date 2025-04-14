@echo off
cd /d D:\ai_trading_streamlit
echo [%date% %time%] 🔧 simulated_trades.json 정리 시작...
.\.venv\Scripts\python.exe fix_simulated_json.py
echo 🔁 완료! 파일 정리가 끝났습니다.
pause
