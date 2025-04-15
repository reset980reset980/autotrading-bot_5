# 📁 파일명: modules/optuna_tuner.py
# 🎯 목적: Optuna를 사용해 전략 매개변수(TP, SL 등)를 자동으로 최적화
# 🔁 전체 흐름도:
#     - 과거 거래 데이터를 기반으로 수익률 최대화 조건 탐색
#     - Optuna로 하이퍼파라미터 탐색 수행
#     - 최적 TP, SL, 진입 조건을 추천
# 🔧 주요 함수:
#     - optimize_strategy(): Optuna 기반 튜닝 실행
#     - objective(): 수익률 기준 목적 함수
# 💬 작업 프롬프트 요약:
#     ▶ "과거 전략 수익률을 기준으로 take_profit, stop_loss 비율을 튜닝하라."

import optuna
import json

def load_simulation_data():
    with open("logs/simulation/simulated_trades.json", "r", encoding="utf-8") as f:
        return json.load(f)

def objective(trial):
    data = load_simulation_data()
    tp = trial.suggest_float("tp", 0.5, 3.0)

    win = 0
    loss = 0
    for trade in data:
        if trade["signal"] == "hold":
            continue
        simulated_profit = tp if trade["profit"] > 0 else -sl
        if simulated_profit > 0:
            win += 1
        else:
            loss += 1

    total = win + loss
    if total == 0:
        return 0
    win_rate = win / total
    return (tp * win_rate) - (sl * (1 - win_rate))


# Optuna 최적화 실행
def optimize_strategy(n_trials=30):
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)

    print("🏁 최적화 완료:")
    print("Best Params:", study.best_params)
    print("Best Score:", study.best_value)
    return study.best_params

# ✅ 단독 실행 예시
if __name__ == "__main__":
    best = optimize_strategy()
