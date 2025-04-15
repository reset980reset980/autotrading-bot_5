# 📁 파일명: modules/strategy_generator.py
# 🎯 목적: 기술 지표 + 감정 점수를 기반으로 AI가 직접 전략 방향을 생성
# 🔁 전체 흐름도:
#     - 기술 지표, 감정 점수, 뉴스 요약을 기반으로 프롬프트 구성
#     - AI 모델(Grok / GPT 등)에게 전략 요청
#     - 전략 응답 → signal, TP, SL 추출 후 전략 생성
# 🔧 주요 함수:
#     - generate_ai_strategy(): AI 프롬프트로 전략 응답 요청
#     - parse_ai_response(): 응답에서 핵심 요소 추출
# 💬 작업 프롬프트 요약:
#     ▶ "RSI, MACD, 감정 점수를 기반으로 오늘의 매매 전략을 판단하라. 방향(HOLD/LONG/SHORT)과 익절/손절 기준도 제시하라."

from modules.ai_model import query_grok

def generate_ai_strategy(rsi: float, macd: float, sentiment: float, bb: str = "중앙") -> str:
    prompt = f"""
    아래는 시장의 기술적 지표와 심리 상태입니다:
    - RSI: {rsi}
    - MACD: {macd}
    - 볼린저밴드 위치: {bb}
    - 감정 점수: {sentiment}

    위 정보를 바탕으로,
    📌 'LONG', 'SHORT', 'HOLD' 중 하나의 전략 방향을 판단하고,
    🎯 익절(Take Profit)과 손절(Stop Loss) 기준(%)을 숫자로 함께 제시하라.

    형식 예시:
    전략: LONG
    익절: 1.5
    손절: 0.5
    이유: RSI가 과매도이며 감정 점수가 긍정적으로 전환되었기 때문.
    """

    return query_grok(prompt)

def parse_ai_response(response: str) -> dict:
    """
    AI 응답에서 전략 요소 추출
    """
    lower = response.lower()
    signal = "hold"
    if "long" in lower and "short" not in lower:
        signal = "long"
    elif "short" in lower and "long" not in lower:
        signal = "short"

    def extract_value(keyword):
        for line in response.splitlines():
            if keyword.lower() in line.lower():
                try:
                    return float(''.join(c for c in line if (c.isdigit() or c == '.')))
                except:
                    return 0.0
        return 0.0

    tp = extract_value("익절")
    sl = extract_value("손절")

    return {
        "signal": signal,
        "tp": round(tp, 2),
        "sl": round(sl, 2),
        "raw_response": response
    }

# ✅ 단독 테스트용
if __name__ == "__main__":
    response = generate_ai_strategy(25.5, -12.8, 0.3, "하단")
    print("🧠 AI 응답:\n", response)
    result = parse_ai_response(response)
    print("📊 파싱 결과:", result)
