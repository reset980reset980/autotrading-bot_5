"""
파일명: models/deep_config.py
목적: 딥러닝 및 예측에 사용되는 설정값 정의
기능:
  - 모델 경로 및 스케일러 경로
  - 학습 파라미터 (에포크, 배치 크기, 분기 기준)
  - 예측 신호 기준점 (thresholds)
  - 미래 확장성을 고려한 하이퍼파라미터 모음

전체 흐름도:
  이 모듈의 설정 → trainer.py, predictor.py, model_utils.py에서 공통 참조

사용 프롬프트 요약:
  ▶ "딥러닝 학습과 예측에 필요한 설정값을 하나의 모듈에서 정의하고 재사용하라."
"""

# 📁 파일 경로
MODEL_PATH = "models/trained_model.h5"
SCALER_PATH = "models/scaler.pkl"
SIMULATION_LOG_PATH = "logs/simulation/simulated_trades.json"

# 🧠 학습 관련 파라미터
EPOCHS = 20
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2
PATIENCE = 3  # EarlyStopping

# 🎯 예측 결과 해석 기준
THRESHOLD_LONG = 0.6
THRESHOLD_SHORT = 0.4

# 💬 학습 로그 출력 여부
VERBOSE = 1

# 향후 추가 가능:
# LEARNING_RATE = 0.001
# OPTUNA_TUNING = True
