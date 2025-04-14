import os
import subprocess
import requests

# ====== 사용자 설정 ======
project_path = r"D:\ai_trading_streamlit"
commit_msg = "🆕 자동 커밋: 최신 변경사항 백업"
from dotenv import load_dotenv
load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

# ========================

def ensure_gitignore():
    gitignore_path = os.path.join(project_path, ".gitignore")
    patterns = [".venv/", ".env", "__pycache__/", "*.pyc"]

    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write("\n".join(patterns))
    else:
        with open(gitignore_path, "r+", encoding="utf-8") as f:
            lines = f.read().splitlines()
            for p in patterns:
                if p not in lines:
                    f.write(f"\n{p}")

def update_requirements():
    req_path = os.path.join(project_path, "requirements.txt")
    subprocess.run(f"{project_path}\\.venv\\Scripts\\python -m pip freeze > {req_path}", shell=True)

def git_push():
    cmds = [
        f"cd /d {project_path}",
        "git add .",
        f'git commit -m "{commit_msg}"',
        "git push"
    ]
    subprocess.run(" && ".join(cmds), shell=True)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

# === 실행 순서 ===
ensure_gitignore()
update_requirements()
try:
    git_push()
    send_telegram("✅ GitHub 백업이 완료되었습니다!")
except Exception as e:
    send_telegram(f"❌ GitHub 백업 실패: {e}")
