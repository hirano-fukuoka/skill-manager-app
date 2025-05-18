import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")
st.title("🎓 資格・認定管理")

# --- データ読み込み ---
df = pd.read_csv("data/certs.csv")
df["有効期限"] = pd.to_datetime(df["有効期限"], format="%Y-%m-%d")
today = pd.Timestamp.today()

# --- 表示用の日付（年月日のみ）を作成 ---
df_display = df.copy()
df_display["有効期限"] = df_display["有効期限"].dt.strftime('%Y-%m-%d')

# --- 期限切れ一覧 ---
st.subheader("⏰ 有効期限切れ資格一覧")
expired = df[df["有効期限"] < today]
st.dataframe(df_display[df["有効期限"] < today]) if not expired.empty else st.success("期限切れの資格はありません。")

# --- 期限30日以内 ---
st.subheader("⚠️ 有効期限が30日以内の資格")
warning = df[(df["有効期限"] >= today) & (df["有効期限"] <= today + pd.Timedelta(days=30))]
st.dataframe(df_display[warning.index]) if not warning.empty else st.info("期限が近い資格はありません。")

# --- 全体表示 ---
st.subheader("📋 全資格一覧")
st.dataframe(df_display.sort_values("有効期限"))
