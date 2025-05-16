import streamlit as st
import pandas as pd

st.header("👤 個人のスキル・資格・教育履歴")

emp = st.selectbox("社員選択", pd.read_csv("data/employees.csv")["社員名"].unique())

st.subheader("🧠 スキル一覧")
st.dataframe(pd.read_csv("data/skills.csv").query("社員名 == @emp"))

st.subheader("📚 教育履歴")
st.dataframe(pd.read_csv("data/training.csv").query("受講者 == @emp"))

st.subheader("🎓 資格一覧")
st.dataframe(pd.read_csv("data/certs.csv").query("社員名 == @emp"))
