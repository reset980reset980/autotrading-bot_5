# 📁 파일명: modules/__init__.py
# 🧩 목적: 모듈 패키지 초기화 및 주요 함수 바로 import 가능하도록 설정
# ✅ 포함 함수:
#   - sentiment 분석
#   - 기술 지표 계산
#   - 환경 설정 로딩
#   - 토큰/수수료 추적
#   - 매매 실행 함수

"""
이 모듈은 modules 폴더 내 서브 모듈들을 외부에서 직접 import 가능하도록 연결합니다.
- 불필요한 경로 오류 방지
- 실제 사용되는 모듈만 import
"""

# 주요 실행 관련 모듈
from modules.grok_bridge import query_grok
from modules.exchange_router import route_trade
from modules.testnet_executor import execute_bybit_test_trade  # ✅ 실제 정의된 함수명
from modules.real_executor import execute_bitget_real_trade
from modules.visualizer import plot_sentiment_trend, plot_strategy_signals

# 로그 및 통계
from modules.logger import log_trade_result, log_daily_summary, save_json_log

# 계정 상태 조회
from modules.account_status import get_wallet_summary

# 전략 분석 및 시뮬레이터
from modules.strategy_generator import generate_ai_strategy as generate_strategy_from_ai
from modules.strategy_flow_chart import draw_strategy_flow

# 알림
from modules.telegram_notifier import send_telegram_message
