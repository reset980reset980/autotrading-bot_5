from ai_core.grok_bridge import get_grok_response

prompt = "비트코인 시장이 지금 하락 중인데, 투자자들은 어떤 반응을 보이고 있지?"

# test with latest model
result = get_grok_response(prompt, model="grok-3-latest")

print("🔹 전략 응답:", result["content"])
print("🧠 Reasoning:", result["reasoning"])
print("💰 사용된 토큰:", result["tokens"])
