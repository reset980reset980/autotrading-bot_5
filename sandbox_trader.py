# 📁 파일명: sandbox_trader.py
# 🎯 목적: Grok + 딥러닝 + 커뮤니티 기반 전략 테스트 및 시뮬레이션
# 🔄 15분 루프 실행 구조로, 실제 매매 대신 로그/시뮬레이션 기반 전략을 기록
# 📚 구성 요소:
#   - 지표 + 뉴스 수집
#   - Grok 응답 기반 전략 판단
#   - HOLD 시 보완 전략 적용
#   - 딥러닝/커뮤니티 필터 반영
#   - 가상매매 수익 시뮬레이션
# 💬 프롬프트:
#   ▶ "현재 지표와 뉴스 감정 기반으로 전략을 판단하고, 보완 전략 및 딥러닝 보조, 커뮤니티 반응까지 종합하여 매매 시뮬레이션을 실행하라."

import time
from utils.indicators import get_indicators
from utils.news_fetcher import fetch_news
from utils.sentiment import analyze_news
from utils.strategy_analyzer import (
    analyze_strategy, analyze_strategy_with_context,
    apply_model_correction, apply_community_adjustment
)
from utils.trade_simulator import simulate_trade, record_trade_log, record_daily_summary
from datetime import datetime

INTERVAL_MINUTES = 15  # 전략 실행 간격

while True:
    print(f"\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 전략 실행 시작 -----------------------------")

    try:
        # 1. 기술 지표 + 뉴스 + 감정 분석
        indicators = get_indicators("BTC/USDT", "15m")
        news_list = fetch_news()
        sentiment_score = analyze_news(news_list) if news_list else 0.35

        # 2. 전략 판단 (Grok)
        prompt = f"""
        Technical Indicators:
        RSI: {indicators['rsi']}, BB: {indicators['bb']}, EMA: {indicators['ema']}, TEMA: {indicators['tema']}, MACD: {indicators['macd']}
        Market Sentiment: {sentiment_score}
        Based on the above, should we go LONG, SHORT, or HOLD?
        """
        try:
            from modules.grok_bridge import query_grok
            ai_response = query_grok(prompt)
        except Exception as e:
            print(f"⚠️ Grok 호출 실패: {e}")
            ai_response = "HOLD"

        # 3. Grok 전략 분석
        core, summary = analyze_strategy(ai_response, indicators, sentiment_score)
        print(f"📩 AI 응답: {ai_response}")
        print(f"📊 전략 판단 결과: {core}")
        print(f"🧠 판단 요약: {summary}")

        # 4. HOLD → 보완 전략 실행
        if core["signal"] == "hold":
            print("🤔 HOLD 응답 → 상위 프레임 기반 보완 전략 적용 중...")
            fallback_core = analyze_strategy_with_context(sentiment_score)
            print(f"📈 보완된 전략 판단: {fallback_core}")
            core = fallback_core  # 덮어쓰기

        # 5. 딥러닝 모델 기반 보완
        core["signal"] = apply_model_correction(core["signal"], indicators, sentiment_score)

        # 6. 커뮤니티 감정 기반 필터링
        core["signal"] = apply_community_adjustment(core["signal"])

        # 7. 매매 시뮬레이션 실행
        if core["signal"] in ["long", "short"]:
            profit = simulate_trade(core["signal"], core["entry_price"], core["tp"], core["sl"])
            core["profit"] = profit
            record_trade_log(core)
            record_daily_summary()
            print(f"💰 매매 시뮬레이션 기록됨 | 수익: {profit:.2f}")
        else:
            print("⏸️ 전략 HOLD → 매매 미실행")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

    print(f"⏳ 다음 실행까지 {INTERVAL_MINUTES}분 대기 중...\n")
    time.sleep(INTERVAL_MINUTES * 60)
