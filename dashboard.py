import streamlit as st
import pandas as pd
import plotly.express as px
import os


def show_dashboard():

    st.header("📊 Resume Analytics Dashboard")

    if not os.path.exists("history.csv"):
        st.warning("No history found.")
        return

    df = pd.read_csv("history.csv")

    total = len(df)
    highest = df["ATS Score"].max()
    average = round(df["ATS Score"].mean(), 2)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📄 Total Resumes", total)

    with col2:
        st.metric("⭐ Highest Score", highest)

    with col3:
        st.metric("📊 Average Score", average)

    st.divider()

    fig = px.bar(
        df,
        x="Name",
        y="ATS Score",
        color="ATS Score",
        title="ATS Score Comparison"
    )

    st.plotly_chart(fig, width="stretch")

    st.divider()

    st.subheader("📋 Resume History")

    st.dataframe(df, width="stretch")