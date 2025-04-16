# 📁 파일명: sandbox_trader.py
# 🎯 목적: Grok + 딥러닝 + 커뮤니티 기반 전략 테스트 및 시뮬레이션
# 🔄 15분 루프 실행 구조로, 실제 매매 대신 로그/시뮬레이션 기반 전략을 기록
# 💬 프롬프트:
#     ▶ "현재 지표와 뉴스 감정 기반으로 전략을 판단하고, 보완 전략 및 딥러닝 보조, 커뮤니티 반응까지 종합하여 매매 시뮬레이션을 실행하라."

import time
from datetime import datetime

from utils.indicators import get_indicators
from utils.news_fetcher import fetch_news
from utils.sentiment import analyze_news
from utils.strategy_analyzer import (
    analyze_strategy,
    analyze_strategy_with_context,
    apply_model_correction,
    apply_community_adjustment
)
from utils.trade_simulator import simulate_trade, record_trade_log, record_daily_summary
from modules.grok_bridge import query_grok
from modules.telegram_notifier import notify_trade_result, notify_system_event  # ← 시스템용 함수 포함

INTERVAL_MINUTES = 15

while True:
    print(f"\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 전략 실행 시작 -----------------------------")
    
    try:
        indicators = get_indicators("BTC/USDT", "15m")
        news_list = fetch_news()
        sentiment_score = analyze_news(news_list) if news_list else 0.35

        prompt = f"""
        Technical Indicators:
        RSI: {indicators['rsi']}, BB: {indicators['bb']}, EMA: {indicators['ema']}, TEMA: {indicators['tema']}, MACD: {indicators['macd']}
        Market Sentiment: {sentiment_score}
        Should we go LONG, SHORT, or HOLD?
        """
        try:
            ai_response = query_grok(prompt)
        except Exception as e:
            error_msg = f"Grok 호출 실패: {e}"
            print(f"⚠️ {error_msg}")
            notify_system_event("Grok 호출 실패", error_msg)
            ai_response = "HOLD"

        core, summary = analyze_strategy(ai_response, indicators, sentiment_score)
        print(f"📩 AI 응답: {ai_response}")
        print(f"📊 전략 판단 결과: {core}")
        print(f"🧠 판단 요약: {summary}")

        if core["signal"] == "hold":
            print("🤔 HOLD → 보완 전략 실행 중...")
            fallback_core = analyze_strategy_with_context(sentiment_score)
            print(f"📈 보완 전략 결과: {fallback_core}")
            core = fallback_core

        try:
            core["signal"] = apply_model_correction(core["signal"], indicators, sentiment_score)
        except Exception as e:
            error_msg = f"딥러닝 예측 오류: {e}"
            print(f"⚠️ {error_msg}")
            notify_system_event("딥러닝 예측 실패", error_msg)
            core["signal"] = "hold"

        core["signal"] = apply_community_adjustment(core["signal"])

        if core["signal"] in ["long", "short"]:
            profit = simulate_trade(core["signal"], core["entry_price"], core["tp"], core["sl"])
            core["profit"] = profit
            record_trade_log(core)
            record_daily_summary()
            print(f"💰 매매 시뮬레이션 기록됨 | 수익: {profit:.2f}")

            notify_trade_result(core, {
                "result": "SIMULATED",
                "pnl": profit,
                "balance": "N/A"
            })

        else:
            print("⏸️ 전략 HOLD → 매매 미실행")

    except Exception as e:
        error_msg = f"❌ 전체 오류 발생: {e}"
        print(error_msg)
        notify_system_event("전체 시스템 오류", error_msg)

    print(f"⏳ 다음 실행까지 {INTERVAL_MINUTES}분 대기...\n")
    time.sleep(INTERVAL_MINUTES * 60)