import streamlit as st
import pandas as pd
import datetime
import os

st.header("📝 教育履歴登録フォーム")

emp_list = pd.read_csv("data/employees.csv")["社員名"].unique()

with st.form("training_form"):
    date = st.date_input("実施日", datetime.date.today())
    content = st.text_input("教育内容")
    emp = st.selectbox("受講者", emp_list)
    status = st.selectbox("ステータス", ["受講済", "未受講"])
    submit = st.form_submit_button("登録")

    if submit:
        df = pd.read_csv("data/training.csv")
        new = pd.DataFrame([[date, content, emp, status]], columns=df.columns)
        df = pd.concat([df, new], ignore_index=True)
        df.to_csv("data/training.csv", index=False)
        st.success("登録完了！")
