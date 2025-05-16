import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.header("📊 スキルマップとギャップ分析")
df = pd.read_csv("data/skills.csv")
ideal = pd.read_csv("data/ideal_skills.csv").set_index("スキル名")

# ヒートマップ
st.subheader("スキルヒートマップ")
df_skills = df.set_index("社員名")
fig, ax = plt.subplots(figsize=(10, len(df_skills)*0.5))
sns.heatmap(df_skills, annot=True, cmap="Blues", fmt="g", ax=ax)
st.pyplot(fig)

# ギャップ分析
st.subheader("スキルギャップ")
for i, row in df.iterrows():
    name = row["社員名"]
    levels = row.drop("社員名")
    diff = ideal["必要レベル"] - levels
    st.write(f"### {name}")
    st.dataframe(diff.to_frame(name="ギャップ"))
