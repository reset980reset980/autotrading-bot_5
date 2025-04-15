# 📁 파일명: utils/data_cleaner.py
# 🎯 목적: 전략 판단을 위한 데이터 정제 및 모델 입력 전처리
# 🔄 순환 참조 방지:
#     - strategy_analyzer의 run_strategy, get_strategy_summary 함수는
#       직접 import 시 순환 참조가 발생하므로 지연 로딩 방식으로 처리
# 🧠 주요 함수:
#     - preprocess_single_entry(): 모델 예측을 위한 단일 데이터 전처리
#     - run_strategy_safe(): strategy_analyzer의 run_strategy 함수 우회 호출
#     - get_strategy_summary_safe(): strategy_analyzer의 get_strategy_summary 함수 우회 호출

def run_strategy_safe(*args, **kwargs):
    """strategy_analyzer.run_strategy 함수 지연 로딩"""
    from utils.strategy_analyzer import run_strategy
    return run_strategy(*args, **kwargs)

def get_strategy_summary_safe(*args, **kwargs):
    """strategy_analyzer.get_strategy_summary 함수 지연 로딩"""
    from utils.strategy_analyzer import get_strategy_summary
    return get_strategy_summary(*args, **kwargs)

def preprocess_single_entry(entry: dict) -> dict:
    """
    딥러닝 예측을 위한 단일 입력 데이터 전처리
    - 필요한 항목만 추출하여 모델 입력 형태로 변환
    """
    return {
        "rsi": entry.get("rsi", 0.0),
        "macd": entry.get("macd", 0.0),
        "ema": entry.get("ema", 0.0),
        "tema": entry.get("tema", 0.0),
        "sentiment": entry.get("sentiment", 0.0),
    }

# ✅ 예시용 테스트 실행 (단독 실행 시)
if __name__ == "__main__":
    test_data = {
        "rsi": 55.2,
        "macd": 8.3,
        "ema": 27400,
        "tema": 27500,
        "sentiment": 0.25,
    }
    print("📦 전처리 결과:", preprocess_single_entry(test_data))
