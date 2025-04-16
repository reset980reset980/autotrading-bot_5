import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# 테스트용 API 키 로딩
api_key = os.getenv("OPENAI_API_KEY")  # 환경변수명 확인
if not api_key:
    raise ValueError("API 키가 누락되었습니다. .env 또는 환경변수에 OPENAI_API_KEY를 설정해주세요.")

# 클라이언트 인스턴스 생성
client = OpenAI(
    api_key=api_key,
    base_url="https://api.openai.com/v1"  # 만약 실제 xAI API가 있다면 여기를 수정
)

# 테스트 프롬프트 실행
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # grok-3이 실제 존재하지 않음
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "이 전략은 롱인가요 숏인가요?"}
        ],
        temperature=0.3
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"❌ API 호출 실패: {e}")
