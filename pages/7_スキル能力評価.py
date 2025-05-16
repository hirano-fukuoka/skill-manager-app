import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
st.title("🧠 スキル能力評価（累積ポイントベース）")

# --- データ読み込み ---
df_points = pd.read_csv("data/skill_points.csv")
df_usage = pd.read_csv("data/skill_usage.csv")
df_levels = pd.read_csv("data/level_thresholds.csv").sort_values("ポイント下限")

# --- スキルごとの貢献ポイントを計算 ---
df_merged = pd.merge(df_usage, df_points, on="スキル名")
df_merged["貢献ポイント"] = df_merged["利用率（0-1）"] * df_merged["ポイント係数"] * 10  # 例：10回分換算

# --- 個人別に累積ポイントを集計 ---
df_total = df_merged.groupby("社員名")["貢献ポイント"].sum().reset_index()
df_total.rename(columns={"貢献ポイント": "トータルポイント"}, inplace=True)

# --- スキルレベル算出 ---
def determine_level(point):
    for _, row in df_levels.iterrows():
        if point < row["ポイント下限"]:
            return int(row["レベル"]) - 1
    return int(df_levels["レベル"].max())

df_total["スキルレベル"] = df_total["トータルポイント"].apply(determine_level)

# --- トップ者にアイコンマーク追加 ---
top_level = df_total["スキルレベル"].max()
df_total["ランク"] = df_total["スキルレベル"].apply(lambda x: "🎖" if x == top_level else "")

# --- レベルフィルタ ---
level_filter = st.multiselect("🎯 表示するスキルレベル", options=sorted(df_total["スキルレベル"].unique(), reverse=True), default=None)

if level_filter:
    df_total = df_total[df_total["スキルレベル"].isin(level_filter)]

# --- 表示（スキルレベル順） ---
st.subheader("📋 スキル評価一覧（スキルレベル順）")

df_total_sorted = df_total.sort_values(by=["スキルレベル", "トータルポイント"], ascending=[False, False])
df_total_sorted = df_total_sorted[["社員名", "トータルポイント", "スキルレベル", "ランク"]]
st.dataframe(df_total_sorted, use_container_width=True)

# --- Altairによる棒グラフ表示 ---
st.subheader("📈 スキルレベル別 トータルポイント比較")

chart = alt.Chart(df_total_sorted).mark_bar().encode(
    x=alt.X("社員名:N", sort="-y"),
    y=alt.Y("トータルポイント:Q"),
    color=alt.Color("スキルレベル:O", scale=alt.Scale(scheme="blues"))
).properties(width=800, height=400)

st.altair_chart(chart, use_container_width=True)

# --- 詳細：各スキルごとの利用と貢献ポイント ---
st.subheader("📊 各スキルの貢献ポイント明細")
st.dataframe(df_merged[["社員名", "スキル名", "利用率（0-1）", "ポイント係数", "貢献ポイント"]], use_container_width=True)
