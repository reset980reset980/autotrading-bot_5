# 📁 파일명: utils/log_cleaner.py
# 🎯 목적: 로그 파일에서 result 누락 항목 자동 보완 및 저장
# 🔁 전체 흐름도:
#     - JSON 로그 파일 읽기
#     - enrich_logs() 호출하여 result 보완
#     - 새로운 파일로 저장 또는 원본 덮어쓰기
# 🔧 주요 함수:
#     - clean_log_file(): 파일 기반 정제 수행
# 💬 작업 프롬프트 요약:
#     ▶ "simulated_trades.json 파일의 로그를 정제하여 분석 가능하게 만든다."

import os
import sys
import json

# 🔧 현재 경로 기준으로 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.trade_result_parser import enrich_logs

def clean_log_file(input_path: str, output_path: str = None, overwrite: bool = False) -> str:
    """
    로그 파일에서 result 필드를 보완하여 저장합니다.

    Args:
        input_path (str): 원본 로그 파일 경로
        output_path (str): 결과 저장 경로 (없으면 input_path + '_cleaned.json')
        overwrite (bool): 원본 덮어쓸지 여부

    Returns:
        str: 저장된 파일 경로
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"파일이 존재하지 않습니다: {input_path}")

    with open(input_path, 'r', encoding='utf-8') as f:
        logs = json.load(f)

    cleaned_logs = enrich_logs(logs)

    # 저장 경로 결정
    save_path = input_path if overwrite else (output_path or input_path.replace(".json", "_cleaned.json"))

    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_logs, f, ensure_ascii=False, indent=2)

    print(f"✅ 정제된 로그가 저장되었습니다: {save_path}")
    return save_path


# ✅ 예시 실행
if __name__ == "__main__":
    # 기본 테스트 로그 경로
    input_file = "logs/simulation/simulated_trades.json"
    clean_log_file(input_path=input_file)
