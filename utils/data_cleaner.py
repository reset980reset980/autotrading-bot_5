# 📁 파일명: utils/data_cleaner.py
# 🎯 목적: 전략 판단을 위한 데이터 정제 및 모델 입력 전처리
# 🔄 strategy_analyzer와의 순환 참조 방지를 위해 지연 로딩 방식 사용

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

# ✅ 예시
if __name__ == "__main__":
    test = {"rsi": 55.2, "macd": 2.1, "ema": 28000, "tema": 28100, "sentiment": 0.12}
    print("전처리 결과:", preprocess_single_entry(test))
