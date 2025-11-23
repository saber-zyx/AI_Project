import streamlit as st
import overview
import bot_analytics
import bot_details

st.set_page_config(
    page_title="ZaloPay Bot Detection",
    layout="wide",
    initial_sidebar_state="expanded"
)

menu = st.sidebar.radio(
    "📌 Chọn mục:",
    ["Tổng quan", "Phân tích Bot", "Chi tiết Bot User"]
)

if menu == "Tổng quan":
    overview.render()
elif menu == "Phân tích Bot":
    bot_analytics.render()
elif menu == "Chi tiết Bot User":
    bot_details.render()
