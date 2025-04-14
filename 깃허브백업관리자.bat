@echo off
cd /d D:\ai_trading_streamlit

REM 가상환경 활성화
call .venv\Scripts\activate.bat

REM 백업 매니저 실행
python git_backup_manager.py

REM 대기 (종료 방지용)
pause
