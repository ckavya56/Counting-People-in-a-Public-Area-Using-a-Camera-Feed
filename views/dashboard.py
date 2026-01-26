import streamlit as st

def show_dashboard(count):
    st.title("Crowd Counting Dashboard")
    st.metric("People Count", count)

    if count > 10:
        st.error("⚠️ Overcrowding Detected!")
