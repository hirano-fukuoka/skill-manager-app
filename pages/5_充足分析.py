import streamlit as st
import pandas as pd

st.header("📈 スキルの充足状況")

df = pd.read_csv("data/needs.csv")
df["差"] = df["保有者数"] - df["必要人数"]

st.dataframe(df)

st.bar_chart(df.set_index("スキル名")["差"])
