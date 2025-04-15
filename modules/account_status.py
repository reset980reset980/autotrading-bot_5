# Sample Python module

def example():
    print('This is a sample.')
"""
파일명: modules/account_status.py
목적: 거래소 API를 통해 자산 현황, 트랜스퍼 내역, 매매 가능 금액 등을 요약 제공
대상: Bybit 테스트넷 (추후 Bitget 확장 예정)
함수 목록:
  - get_wallet_summary(): 현재 자산 잔고 요약
  - get_transfer_history(): 입출금 및 이체 내역 요약
  - get_trading_available_amount(): 매매 가능 금액 계산
  - check_margin_status(): 마진 사용률 및 위험 진단
"""

from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv

load_dotenv()

# Bybit 테스트넷 인증정보
BYBIT_API_KEY = os.getenv("BYBIT_TESTNET_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_TESTNET_API_SECRET")

session = HTTP(
    testnet=True,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET
)

def get_wallet_summary():
    try:
        result = session.get_wallet_balance(accountType="UNIFIED")
        balances = result['result']['list'][0]['coin']
        return {coin['coin']: coin['equity'] for coin in balances if float(coin['equity']) > 0}
    except Exception as e:
        return {"error": str(e)}

def get_trading_available_amount(symbol="BTCUSDT"):
    try:
        result = session.get_available_balance(accountType="UNIFIED")
        return result.get("result", {}).get("availableBalance", 0.0)
    except Exception as e:
        return {"error": str(e)}

def get_transfer_history(limit=5):
    try:
        result = session.get_wallet_fund_records(category="TRANSFER", limit=limit)
        return result.get("result", {}).get("rows", [])
    except Exception as e:
        return {"error": str(e)}

def check_margin_status():
    try:
        result = session.get_risk_limit()
        return result.get("result", {})
    except Exception as e:
        return {"error": str(e)}
