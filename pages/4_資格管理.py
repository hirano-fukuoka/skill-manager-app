import streamlit as st
import pandas as pd

st.header("🎓 資格・認定管理")

df = pd.read_csv("data/certs.csv")
df["有効期限"] = pd.to_datetime(df["有効期限"])
df_expired = df[df["有効期限"] < pd.Timestamp.today()]

st.subheader("⏰ 有効期限切れ資格")
st.dataframe(df_expired)

st.subheader("📋 全資格一覧")
st.dataframe(df)
