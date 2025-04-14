
📦 백업 자동화 세트 - 사용 설명서 (README)

이 폴더는 AI 자동매매 시스템의 GitHub 자동 백업 및 동기화를 위한 도구 모음입니다.

✅ 포함 파일 설명:

1. auto_git_backup.bat
   - 민감 파일 제거 (.env, .venv 등)
   - .gitignore 반영 후 Git 커밋 및 푸시

2. auto_git_backup.py
   - 파이썬 기반 자동 백업 스크립트
   - requirements.txt 자동 갱신
   - 텔레그램 알림 기능 포함

3. git_backup.bat
   - 수동으로 전체 변경사항 백업할 때 사용

4. requirements.txt
   - 프로젝트 의존성 목록

5. update_from_github.bat
   - GitHub에서 코드 최신화 (git pull)
   - 동기화 로그(sync_log.txt)에 기록됨

🕑 추천 사용 흐름:

- 오전: `update_from_github.bat` 실행하여 최신 코드 반영
- 퇴근 전: `auto_git_backup.py` 또는 `git_backup.bat` 실행하여 백업

