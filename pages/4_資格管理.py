import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")
st.title("🎓 資格・認定管理")

# --- データ読み込み ---
df = pd.read_csv("data/certs.csv")
df["有効期限"] = pd.to_datetime(df["有効期限"], format="%Y-%m-%d")
today = pd.Timestamp.today()

# --- 期限切れ一覧 ---
df_expired = df[df["有効期限"] < today]

st.subheader("⏰ 有効期限切れ資格一覧")
if df_expired.empty:
    st.success("期限切れの資格はありません。")
else:
    st.dataframe(df_expired)

# --- 有効期限が近い（30日以内） ---
st.subheader("⚠️ 有効期限が30日以内の資格")
df_warning = df[(df["有効期限"] >= today) & (df["有効期限"] <= today + pd.Timedelta(days=30))]
if df_warning.empty:
    st.info("期限が近い資格はありません。")
else:
    st.dataframe(df_warning)

# --- 全体一覧 ---
st.subheader("📋 全資格一覧")
st.dataframe(df.sort_values("有効期限"))
