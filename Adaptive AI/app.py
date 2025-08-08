import streamlit as st
import Home, performance, Settings

st.set_page_config(page_title="Adaptive AI Tutor", layout="centered")
st.title("Adaptive AI Tutor")

tab_titles = ["Home", "Performance", "Settings"]
tabs = st.tabs(tab_titles)

with tabs[0]:
    Home.run()

with tabs[1]:
    performance.run()

with tabs[2]:
    Settings.run()
