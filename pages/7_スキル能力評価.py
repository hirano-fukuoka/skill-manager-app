import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
st.title("🧠 スキル能力評価（スキルレベル込み）")

# --- データ読み込み ---
df_points = pd.read_csv("data/skill_points.csv")
df_usage = pd.read_csv("data/skill_usage.csv")
df_levels = pd.read_csv("data/level_thresholds.csv").sort_values("ポイント下限")
df_skill_lv = pd.read_csv("data/skill_levels.csv")

# --- 各データ結合（利用率 × 係数 × スキルレベル）---
df = df_usage.merge(df_points, on="スキル名")
df = df.merge(df_skill_lv, on=["社員名", "スキル名"])
df["貢献ポイント"] = df["利用率（0-1）"] * df["ポイント係数"] * df["スキルレベル"]

# --- 個人ごとに合計ポイント計算 ---
df_total = df.groupby("社員名")["貢献ポイント"].sum().reset_index()
df_total.rename(columns={"貢献ポイント": "トータルポイント"}, inplace=True)

# --- スキルレベル（能力）判定 ---
def determine_level(point):
    for _, row in df_levels.iterrows():
        if point < row["ポイント下限"]:
            return int(row["レベル"]) - 1
    return int(df_levels["レベル"].max())

df_total["スキルレベル"] = df_total["トータルポイント"].apply(determine_level)
top_level = df_total["スキルレベル"].max()
df_total["ランク"] = df_total["スキルレベル"].apply(lambda x: "🎖" if x == top_level else "")

# --- レベルフィルタ ---
level_filter = st.multiselect("🎯 表示するスキルレベル", sorted(df_total["スキルレベル"].unique(), reverse=True))
if level_filter:
    df_total = df_total[df_total["スキルレベル"].isin(level_filter)]

# --- 表示（降順ソート）---
st.subheader("📋 スキル評価一覧（スキルレベル順）")
df_total_sorted = df_total.sort_values(by=["スキルレベル", "トータルポイント"], ascending=[False, False])
st.dataframe(df_total_sorted[["社員名", "トータルポイント", "スキルレベル", "ランク"]], use_container_width=True)

# --- Altair棒グラフ ---
st.subheader("📈 トータルポイント比較")
chart = alt.Chart(df_total_sorted).mark_bar().encode(
    x=alt.X("社員名:N", sort="-y"),
    y=alt.Y("トータルポイント:Q"),
    color=alt.Color("スキルレベル:O", scale=alt.Scale(scheme="blues"))
).properties(width=800, height=400)
st.altair_chart(chart, use_container_width=True)

# --- 明細表示 ---
st.subheader("📊 各スキルの貢献ポイント明細（スキルレベル込み）")
st.dataframe(df[["社員名", "スキル名", "利用率（0-1）", "ポイント係数", "スキルレベル", "貢献ポイント"]], use_container_width=True)
