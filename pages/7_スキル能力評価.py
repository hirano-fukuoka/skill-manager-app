import streamlit as st
import pandas as pd

st.header("🧠 個人スキル評価（累積ポイントベース）")

# CSV読み込み
df_points = pd.read_csv("data/skill_points.csv")
df_usage = pd.read_csv("data/skill_usage.csv")
df_levels = pd.read_csv("data/level_thresholds.csv").sort_values("ポイント下限")

# スキルごとのポイント貢献を計算
df_merged = pd.merge(df_usage, df_points, on="スキル名")
df_merged["貢献ポイント"] = df_merged["利用率（0-1）"] * df_merged["ポイント係数"] * 10  # 例：10回利用換算

# 個人別に合計
df_total = df_merged.groupby("社員名")["貢献ポイント"].sum().reset_index()
df_total.rename(columns={"貢献ポイント": "トータルポイント"}, inplace=True)

# スキルレベル判定
def determine_level(point):
    for _, row in df_levels.iterrows():
        if point < row["ポイント下限"]:
            return int(row["レベル"]) - 1
    return int(df_levels["レベル"].max())

df_total["スキルレベル"] = df_total["トータルポイント"].apply(determine_level)

# 表示
st.subheader("📋 スキル評価結果")
st.dataframe(df_total)

# 詳細：各スキルごとの貢献度
st.subheader("📊 各スキルの貢献ポイント（参考）")
st.dataframe(df_merged[["社員名", "スキル名", "利用率（0-1）", "ポイント係数", "貢献ポイント"]])
