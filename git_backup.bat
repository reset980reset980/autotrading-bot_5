@echo off
chcp 65001 > nul
cd /d D:\ai_trading_streamlit

echo [0/4] GitHub 업로드 제한 대비 zip 파일 제거 중...
git rm --cached *.zip

echo [1/4] 변경된 파일 추가 중...
git add .

echo [2/4] 커밋 중...
git commit -m "🆕 자동 커밋: 최신 변경사항 백업"

echo [3/4] GitHub로 푸시 중...
FOR /F "tokens=*" %%i IN ('git rev-parse --abbrev-ref HEAD') DO set CUR_BRANCH=%%i
git push --set-upstream origin %CUR_BRANCH%

echo.
echo ✅ 백업 완료! 창을 닫아주세요.
pause
