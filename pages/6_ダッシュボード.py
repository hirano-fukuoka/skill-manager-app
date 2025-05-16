import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
st.title("📊 力量レベル分析ダッシュボード")

# --- データ読み込み ---
df_power = pd.read_csv("data/power_level_by_month.csv")
df_growth = pd.read_csv("data/monthly_growth.csv")

# --- フィルタ ---
factories = sorted(df_power["工場"].unique())
categories = sorted(df_power["カテゴリ"].unique())
months = sorted(df_power["年月"].unique())

col1, col2, col3 = st.columns(3)
with col1:
    selected_factory = st.selectbox("🏭 工場選択", options=["全社"] + factories)
with col2:
    selected_category = st.selectbox("🧩 カテゴリ選択", options=["すべて"] + categories)
with col3:
    selected_level = st.multiselect("📈 力量レベル（数値）", options=[1, 2, 3, 4], default=[1, 2, 3, 4])

# --- フィルタ適用 ---
df_filtered = df_power.copy()
if selected_factory != "全社":
    df_filtered = df_filtered[df_filtered["工場"] == selected_factory]
if selected_category != "すべて":
    df_filtered = df_filtered[df_filtered["カテゴリ"] == selected_category]

# --- グラフ：合計推移 ---
st.subheader("📈 力量レベル合計の推移")
chart = alt.Chart(df_filtered).mark_line(point=True).encode(
    x="年月:T",
    y="レベル合計:Q",
    color="工場:N"
).properties(width=700)
st.altair_chart(chart, use_container_width=True)

# --- グラフ：カテゴリ別推移 ---
st.subheader("📈 カテゴリ別合計推移")
chart2 = alt.Chart(df_power).mark_area(opacity=0.5).encode(
    x="年月:T",
    y="レベル合計:Q",
    color="カテゴリ:N"
).properties(width=700)
st.altair_chart(chart2, use_container_width=True)

# --- 棒グラフ：内訳 ---
st.subheader("📊 力量レベルの内訳")
bar_df = df_filtered.groupby(["年月", "工場"]).agg({"レベル合計": "sum"}).reset_index()
chart3 = alt.Chart(bar_df).mark_bar().encode(
    x="年月:T",
    y="レベル合計:Q",
    color="工場:N"
).properties(width=700)
st.altair_chart(chart3, use_container_width=True)

# --- 表：月別伸び率 ---
st.subheader("📋 月別伸び率（前月比 %）")

def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: lightgreen' if v else '' for v in is_max]

st.dataframe(df_growth.style.apply(highlight_max, axis=1), use_container_width=True)

# --- エクスポートオプション ---
st.sidebar.markdown("### 📤 エクスポート")
export_format = st.sidebar.selectbox("ファイル形式", ["CSV", "PDF", "PNG"])
st.sidebar.info(f"{export_format} 出力は今後対応予定です。")
