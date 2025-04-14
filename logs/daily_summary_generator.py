import streamlit as st
import os
from datetime import datetime

LOG_FOLDER = "logs/daily_summaries"

st.set_page_config(page_title="📅 오늘 요약", layout="wide")
st.title("📅 오늘 요약 확인")

if st.button("📅 오늘 요약 보기"):
    today = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(LOG_FOLDER, f"{today}.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            st.text(f.read())
    else:
        st.warning("오늘 요약 파일이 아직 생성되지 않았습니다.")
