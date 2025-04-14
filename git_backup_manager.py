import subprocess
import requests
import os
import logging
import sys
from dotenv import load_dotenv

# 프로젝트 경로 (절대 경로)
PROJECT_PATH = "D:/ai_trading_streamlit"

# 프로그램 시작 시 작업 디렉토리 고정
try:
    os.chdir(PROJECT_PATH)
except Exception as e:
    print(f"❌ 작업 디렉토리 변경 오류: {e}")
    print("프로그램이 D:/ai_trading_streamlit 디렉토리에서 실행되어야 합니다.")
    input("계속하려면 Enter 키를 누르세요...")
    exit(1)

# 로그 파일 설정 (절대 경로)
logging.basicConfig(
    filename=os.path.join(PROJECT_PATH, "backup.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# .env 파일 로드 (절대 경로)
env_path = os.path.join(PROJECT_PATH, ".env")
if not os.path.exists(env_path):
    print(f"❌ .env 파일을 찾을 수 없습니다: {env_path}")
    logging.error(f".env 파일을 찾을 수 없음: {env_path}")
    input("계속하려면 Enter 키를 누르세요...")
    exit(1)

load_dotenv(env_path)

# 환경 변수 로드
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
REPO_PREFIX = "autotrading-bot_"
BRANCH_NAME = "main"

def send_telegram(message: str):
    """Telegram으로 메시지 전송"""
    try:
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            logging.warning("Telegram 설정값이 없습니다.")
            print("⚠️ 텔레그램 설정값이 없습니다.")
            return
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})
        logging.info(f"Telegram 메시지 전송: {message}")
    except Exception as e:
        logging.error(f"Telegram 전송 실패: {e}")
        print(f"⚠️ 텔레그램 전송 실패: {e}")

def run_git_command(command, step=""):
    """Git 명령어 실행"""
    try:
        # Git 인코딩 설정 (커밋 메시지 및 출력 UTF-8 강제)
        subprocess.run(
            "git config --global i18n.commitEncoding utf-8",
            shell=True,
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        subprocess.run(
            "git config --global i18n.logOutputEncoding utf-8",
            shell=True,
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        # 환경 변수 설정으로 인코딩 문제 방지
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["LANG"] = "en_US.UTF-8"

        result = subprocess.run(
            command,
            check=True,
            shell=True,
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env
        )
        logging.info(f"Git 명령 성공 ({step}): {command}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Git 오류 ({step}): {e.stderr}")
        print(f"❌ 오류 발생 ({step}): {e.stderr}")
        send_telegram(f"❌ Git 오류 ({step}) 발생\n{e.stderr}")
        return False, e.stderr
    except Exception as e:
        logging.error(f"Git 명령 실행 오류 ({step}): {e}")
        print(f"❌ Git 명령 실행 오류 ({step}): {e}")
        if "Connection" in str(e) or "network" in str(e).lower():
            print("⚠️ 네트워크 연결 문제를 확인하세요.")
            send_telegram("⚠️ 네트워크 연결 문제 발생")
        send_telegram(f"❌ Git 명령 실행 오류 ({step})\n{e}")
        return False, str(e)

def has_changes():
    """변경 사항 확인 (Untracked files 포함)"""
    try:
        # Untracked files 확인
        status_result = subprocess.run(
            "git status --porcelain",
            shell=True,
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        if "?? " in status_result.stdout:
            untracked_files = [line.split()[1] for line in status_result.stdout.splitlines() if line.startswith('?? ')]
            logging.info("Untracked files 감지됨")
            print(f"ℹ️ Untracked files 감지됨: {untracked_files}")
        
        # git add . 실행하여 Untracked files를 스테이징
        subprocess.run(
            "git add .",
            shell=True,
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        # 변경 사항 확인
        result = subprocess.run(
            "git status --porcelain",
            shell=True,
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        if not result.stdout.strip():
            print("ℹ️ 커밋할 변경 사항이 없습니다. 새 파일을 추가하거나 기존 파일을 수정하세요.")
            logging.info("커밋할 변경 사항 없음")
            send_telegram("ℹ️ 백업: 커밋할 변경 사항이 없습니다.")
            return False
        logging.info("변경 사항 확인됨")
        changed_files = [line.split()[1] for line in result.stdout.splitlines()]
        print(f"ℹ️ 변경된 파일: {changed_files}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"변경 사항 확인 오류: {e.stderr}")
        print(f"❌ 변경 사항 확인 오류: {e.stderr}")
        return False

def auto_backup():
    """자동 백업 실행"""
    print("📁 자동 백업을 시작합니다...")
    logging.info("자동 백업 시작")
    if not has_changes():
        return

    steps = [
        ("Remove .zip", "git rm --cached --ignore-unmatch *.zip > nul 2>&1"),
        ("Add files", "git add ."),
        ("Commit", "git commit -m \"🆕 자동 커밋: 최신 변경사항 백업\""),
        ("Push", f"git push --set-upstream origin {BRANCH_NAME}")
    ]
    for step_name, command in steps:
        success, _ = run_git_command(command, step=step_name)
        if not success:
            return
    print("✅ 자동 백업 완료!")
    logging.info("자동 백업 완료")
    send_telegram("✅ Git 자동 백업 완료되었습니다.")

def manual_backup():
    """수동 백업 실행"""
    print("🧹 수동 백업 (민감파일 정리 후 push)")
    logging.info("수동 백업 시작")
    cleanup_cmds = [
        "git rm --cached --ignore-unmatch .env > nul 2>&1",
        "git rm --cached --ignore-unmatch -r .venv > nul 2>&1",
        "git rm --cached --ignore-unmatch -r .vscode > nul 2>&1",
        "git rm --cached --ignore-unmatch *.log > nul 2>&1",
        "git rm --cached --ignore-unmatch backup_log.txt > nul 2>&1",
        "git rm --cached --ignore-unmatch *.exe > nul 2>&1",
        "git rm --cached --ignore-unmatch *.bat > nul 2>&1",
        "git rm --cached --ignore-unmatch *.spec > nul 2>&1",
        "git rm --cached --ignore-unmatch -r .streamlit > nul 2>&1",
        "git rm --cached --ignore-unmatch *.zip > nul 2>&1",
        "git add .gitignore",
    ]
    for cmd in cleanup_cmds:
        run_git_command(cmd, step="수동 백업 정리")

    if not has_changes():
        return

    success, _ = run_git_command('git commit -m "🔒 수동 정리 백업"', step="Commit")
    if success:
        success, _ = run_git_command(f"git push --set-upstream origin {BRANCH_NAME}", step="Push")
        if success:
            print("✅ 수동 백업 완료!")
            logging.info("수동 백업 완료")
            send_telegram("✅ Git 수동 백업 완료되었습니다.")
        else:
            print("⚠️ 푸시 실패: 수동 백업이 완료되지 않았습니다.")
            logging.warning("수동 백업 푸시 실패")

def create_repo_and_backup():
    """새 레포지토리 생성 및 백업"""
    if not GITHUB_USERNAME:
        print("❌ 오류: GITHUB_USERNAME 환경 변수가 설정되지 않았습니다.")
        logging.error("GITHUB_USERNAME 환경 변수 누락")
        send_telegram("❌ 레포 생성 실패: GITHUB_USERNAME이 설정되지 않음")
        return

    repo_suffix = input("📦 생성할 레포 이름 (숫자만 입력, 예: '3' → autotrading-bot_3): ").strip()
    if not repo_suffix.isdigit():
        print("❌ 오류: 레포 이름은 숫자만 입력해야 합니다.")
        logging.error(f"잘못된 레포 접미사: {repo_suffix}")
        send_telegram("❌ 레포 생성 실패: 숫자만 입력해야 함")
        return

    repo_name = f"{REPO_PREFIX}{repo_suffix}"
    api_url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"name": repo_name, "private": False}
    try:
        res = requests.post(api_url, headers=headers, json=data)
        if res.status_code == 201:
            print(f"✅ 레포지토리 생성 완료: {repo_name}")
            logging.info(f"레포지토리 생성: {repo_name}")
            set_remote_and_push(repo_name)
        else:
            print(f"❌ 레포 생성 실패: {res.text}")
            logging.error(f"레포 생성 실패: {res.text}")
            send_telegram(f"❌ 레포지토리 생성 실패\n{res.text}")
    except Exception as e:
        print(f"❌ 레포 생성 오류: {e}")
        logging.error(f"레포 생성 오류: {e}")
        send_telegram(f"❌ 레포지토리 생성 오류\n{e}")

def set_remote_and_push(repo_name):
    """원격 레포지토리 설정 및 푸시"""
    url = f"https://github.com/{GITHUB_USERNAME}/{repo_name}.git"
    run_git_command("git remote remove origin > nul 2>&1", "Remove origin")
    success, _ = run_git_command(f"git remote add origin {url}", "Add origin")
    if success:
        print(f"✅ Git 원격 저장소 변경 완료: {url}")
        logging.info(f"원격 저장소 설정: {url}")
        auto_backup()

def change_repo():
    """기존 레포지토리 연결 변경"""
    if not GITHUB_USERNAME:
        print("❌ 오류: GITHUB_USERNAME 환경 변수가 설정되지 않았습니다.")
        logging.error("GITHUB_USERNAME 환경 변수 누락")
        send_telegram("❌ 레포 연결 실패: GITHUB_USERNAME이 설정되지 않음")
        return

    repo_suffix = input("🔁 연결할 기존 레포 이름 (숫자만 입력, 예: '3' → autotrading-bot_3): ").strip()
    if not repo_suffix.isdigit():
        print("❌ 오류: 레포 이름은 숫자만 입력해야 합니다.")
        logging.error(f"잘못된 레포 접미사: {repo_suffix}")
        send_telegram("❌ 레포 연결 실패: 숫자만 입력해야 함")
        return

    repo_name = f"{REPO_PREFIX}{repo_suffix}"
    set_remote_and_push(repo_name)

def check_current_repo():
    """현재 연결된 레포지토리 확인"""
    print("🔍 현재 연결된 레포지토리를 확인합니다...")
    logging.info("현재 연결된 레포지토리 확인 시작")
    success, output = run_git_command("git remote -v", step="Check remote")
    if success:
        if output.strip():
            # 첫 번째 줄의 URL만 추출
            remote_url = output.splitlines()[0].split()[1]
            print(f"✅ 현재 연결된 레포지토리: {remote_url}")
            logging.info(f"현재 연결된 레포지토리: {remote_url}")
            send_telegram(f"🔍 현재 연결된 레포지토리: {remote_url}")
        else:
            print("⚠️ 연결된 레포지토리가 없습니다.")
            logging.info("연결된 레포지토리 없음")
            send_telegram("⚠️ 연결된 레포지토리가 없습니다.")
    else:
        print("⚠️ 레포지토리 확인에 실패했습니다.")
        logging.warning("레포지토리 확인 실패")

def delete_repo():
    """GitHub에서 레포지토리 삭제"""
    if not GITHUB_USERNAME:
        print("❌ 오류: GITHUB_USERNAME 환경 변수가 설정되지 않았습니다.")
        logging.error("GITHUB_USERNAME 환경 변수 누락")
        send_telegram("❌ 레포 삭제 실패: GITHUB_USERNAME이 설정되지 않음")
        return

    repo_suffix = input("🗑️ 삭제할 레포 이름 (숫자만 입력, 예: '3' → autotrading-bot_3): ").strip()
    if not repo_suffix.isdigit():
        print("❌ 오류: 레포 이름은 숫자만 입력해야 합니다.")
        logging.error(f"잘못된 레포 접미사: {repo_suffix}")
        send_telegram("❌ 레포 삭제 실패: 숫자만 입력해야 함")
        return

    repo_name = f"{REPO_PREFIX}{repo_suffix}"
    confirm = input(f"⚠️ {repo_name} 레포지토리를 삭제하시겠습니까? (y/n): ").strip().lower()
    if confirm != 'y':
        print("ℹ️ 레포 삭제가 취소되었습니다.")
        logging.info("레포 삭제 취소")
        return

    api_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        res = requests.delete(api_url, headers=headers)
        if res.status_code == 204:
            print(f"✅ 레포지토리 삭제 완료: {repo_name}")
            logging.info(f"레포지토리 삭제: {repo_name}")
            send_telegram(f"🗑️ 레포지토리 삭제 완료: {repo_name}")
        else:
            print(f"❌ 레포 삭제 실패: {res.text}")
            logging.error(f"레포 삭제 실패: {res.text}")
            send_telegram(f"❌ 레포지토리 삭제 실패\n{res.text}")
    except Exception as e:
        print(f"❌ 레포 삭제 오류: {e}")
        logging.error(f"레포 삭제 오류: {e}")
        send_telegram(f"❌ 레포지토리 삭제 오류\n{e}")

def pull_latest():
    """최신 코드 풀"""
    logging.info("최신 코드 풀 시작")
    print("📥 최신 코드 가져오기를 시작합니다...")
    
    # 추적 관계 설정 시도
    run_git_command(
        f"git branch --set-upstream-to=origin/{BRANCH_NAME} {BRANCH_NAME}",
        "Set upstream"
    )
    
    # git pull 실행
    success, _ = run_git_command(f"git pull origin {BRANCH_NAME}", "Pull 최신 코드")
    if success:
        print("✅ 최신 코드 가져오기 완료")
        logging.info("최신 코드 풀 완료")
        send_telegram("📥 최신 코드 pull 완료")
    else:
        print("⚠️ Pull 중 문제가 발생했습니다. 원격 저장소를 확인하세요.")
        logging.warning("Pull 실패")

def open_vscode():
    """Visual Studio Code 실행"""
    try:
        # Visual Studio Code 실행 파일 경로 (동적으로 설정)
        vscode_path = os.path.expandvars(r"%LocalAppData%\Programs\Microsoft VS Code\Code.exe")
        
        # 실행 파일 존재 여부 확인
        if not os.path.exists(vscode_path):
            # 대체 경로 확인 (집에서의 경로)
            alt_vscode_path = "C:/Users/KSD/AppData/Local/Programs/Microsoft VS Code/Code.exe"
            if os.path.exists(alt_vscode_path):
                vscode_path = alt_vscode_path
            else:
                raise FileNotFoundError(f"Visual Studio Code 실행 파일을 찾을 수 없습니다: {vscode_path}")

        # PATH에 code 명령어 등록 여부 확인 (디버깅용)
        path_env = os.environ.get("PATH", "")
        logging.info(f"PATH 환경 변수: {path_env}")
        if "Microsoft VS Code" not in path_env:
            print("⚠️ 경고: PATH에 Visual Studio Code 경로가 포함되어 있지 않습니다.")

        # Visual Studio Code 실행
        subprocess.Popen([vscode_path, "."], cwd=PROJECT_PATH)
        print("🚀 Visual Studio Code 실행됨")
        logging.info("VSCode 실행")

        # Visual Studio Code 실행 후 커맨드 창 닫기
        os._exit(0)
    except Exception as e:
        print(f"❌ VSCode 실행 오류: {e}")
        logging.error(f"VSCode 실행 오류: {e}")
        print("ℹ️ Visual Studio Code 설치 경로를 확인하세요.")
        print("ℹ️ 경로가 맞는지, 파일이 존재하는지 확인하세요.")

def main():
    """메인 메뉴"""
    try:
        if not GITHUB_USERNAME:
            print("❌ 오류: GITHUB_USERNAME 환경 변수가 설정되지 않았습니다. .env 파일을 확인하세요.")
            logging.error("프로그램 시작 실패: GITHUB_USERNAME 누락")
            input("계속하려면 Enter 키를 누르세요...")
            return

        if not GITHUB_TOKEN:
            print("❌ 오류: GITHUB_TOKEN 환경 변수가 설정되지 않았습니다. .env 파일을 확인하세요.")
            logging.error("프로그램 시작 실패: GITHUB_TOKEN 누락")
            input("계속하려면 Enter 키를 누르세요...")
            return

        while True:
            print("\n==============================")
            print("🔄 GitHub 자동 백업 도우미")
            print("==============================")
            print("[1] 기존 레포에 자동 백업 (자동 커밋 + push)")
            print("[2] 기존 레포에 수동 백업 (중간정검용, 민감파일 정리 후 push)")
            print("[3] 새 레포 생성 → 연결 + 자동 백업")
            print("[4] 레포연결 변경하기")
            print("[5] GitHub에서 코드 가져오기 (pull)")
            print("[6] 비쥬얼스튜디오 실행")
            print("[7] 현재 연결된 레포 확인")
            print("[8] GitHub에서 레포 삭제")
            print("[9] 종료\n")

            choice = input("👉 번호를 입력하세요: ").strip()
            logging.info(f"사용자 선택: {choice}")
            if choice == "1":
                auto_backup()
            elif choice == "2":
                manual_backup()
            elif choice == "3":
                create_repo_and_backup()
            elif choice == "4":
                change_repo()
            elif choice == "5":
                pull_latest()
            elif choice == "6":
                open_vscode()
            elif choice == "7":
                check_current_repo()
            elif choice == "8":
                delete_repo()
            elif choice == "9":
                print("👋 종료합니다.")
                logging.info("프로그램 종료")
                break
            else:
                print("❌ 잘못된 입력입니다. 다시 선택해주세요.")
                logging.warning(f"잘못된 입력: {choice}")
    except Exception as e:
        print(f"❌ 예기치 않은 오류 발생: {e}")
        logging.error(f"예기치 않은 오류: {e}")
        input("계속하려면 Enter 키를 누르세요...")

if __name__ == "__main__":
    main()