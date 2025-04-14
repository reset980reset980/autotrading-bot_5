import os
import zipfile
from datetime import datetime

# 기준 경로 설정
base_dir = "D:/ai_trading_streamlit"
folder_name = os.path.basename(base_dir.rstrip("/\\"))
now = datetime.now().strftime("%Y%m%d_%H%M")
zip_filename = f"{folder_name}_{now}.zip"
zip_path = os.path.join(base_dir, zip_filename)

# 사용자 입력 (버전 태그)
version_tag = input("압축할 버전명을 입력하세요 (예: v2, g_v2, base, all): ").strip()
if not version_tag:
    print("\n❌ [오류] 버전명을 입력하지 않아 종료합니다.")
    exit()

version_files = []

for root, dirs, files in os.walk(base_dir):
    # .git, .venv 포함된 경로는 무시
    if any(excluded in root for excluded in [".git", ".venv", "__pycache__"]):
        continue

    for file in files:
        if version_tag == "all":
            match = True
        elif version_tag == "base":
            match = "_v" not in file
        else:
            match = version_tag in file

        if match:
            full_path = os.path.join(root, file)
            arc_name = os.path.relpath(full_path, base_dir)
            version_files.append((full_path, arc_name))

if not version_files:
    print(f"\n⚠️ [경고] '{version_tag}'가 포함된 파일을 찾지 못했습니다. 압축하지 않고 종료합니다.")
    exit()

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for full_path, arc_name in version_files:
        zipf.write(full_path, arcname=arc_name)

print(f"\n✅ 총 {len(version_files)}개의 파일을 압축했습니다.")
print(f"📦 저장 위치: {zip_path}")
