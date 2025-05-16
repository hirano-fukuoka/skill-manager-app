import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📊 スキルレーダーチャート")

# データ読み込み
df_points = pd.read_csv("data/skill_points.csv")
df_usage = pd.read_csv("data/skill_usage.csv")

# 利用率 × 係数 × 10 で貢献ポイント算出
df_merged = pd.merge(df_usage, df_points, on="スキル名")
df_merged["貢献ポイント"] = df_merged["利用率（0-1）"] * df_merged["ポイント係数"] * 10

# ピボット：社員 × スキル別ポイント
df_pivot = df_merged.pivot_table(index="社員名", columns="スキル名", values="貢献ポイント", fill_value=0)

# 表示対象社員選択（複数選択可能）
selected_users = st.multiselect("表示する社員を選択", options=df_pivot.index.tolist(), default=df_pivot.index.tolist())

# レーダーチャート描画
fig = go.Figure()

for user in selected_users:
    values = df_pivot.loc[user].tolist()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],  # 円を閉じる
        theta=list(df_pivot.columns) + [df_pivot.columns[0]],
        fill='toself',
        name=user
    ))

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, df_pivot.max().max() + 10])
    ),
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

# データも併記
st.subheader("📋 スキル別貢献ポイント一覧")
st.dataframe(df_pivot)
