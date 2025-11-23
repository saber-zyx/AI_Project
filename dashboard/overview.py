import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_all_users, load_bot_details


# ================================
#         PAGE RENDER
# ================================
def render():

    # Load data
    df_all = load_all_users()
    df_bot = df_all[df_all["isBot"] == 1]
    df_normal = df_all[df_all["isBot"] == 0]

    # Basic metrics
    total_users = df_all["userID"].nunique()
    total_bots = df_bot["userID"].nunique()
    normal_users = df_normal["userID"].nunique()
    bot_rate = (total_bots / total_users) * 100 if total_users > 0 else 0

    total_loss = df_bot["total_loss"].sum()
    total_normal_amount = df_normal["total_normal_amount"].sum()

    # Title
    st.title("📊 Tổng quan hệ thống")

    st.markdown("### 📌 Tổng quan hệ thống")

    # =====================
    #        KPI GRID
    # =====================
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    # Row 1 KPI
    col1.metric("👥 Tổng số người dùng", f"{total_users:,}")
    col2.metric("🤖 Tổng số Bot User", f"{total_bots:,}")
    col3.metric("🧍 Người dùng bình thường", f"{normal_users:,}")

    # Row 2 KPI
    col4.metric("🔥 Tỷ lệ Bot (%)", f"{bot_rate:.2f} %")
    col5.metric("💸 Tổng thiệt hại do Bot (VND)", f"{total_loss:,.0f}")
    col6.metric("🏦 Tổng khối lượng giao dịch User thường (VND)", f"{total_normal_amount:,.0f}")

    st.markdown("---")

    # =====================
    #      PIE CHART
    # =====================
    st.markdown("### 🥧 Tỷ lệ Bot vs Người dùng bình thường")

    fig_pie = px.pie(
        values=[normal_users, total_bots],
        names=["Normal User", "Bot User"],
        hole=0.45,
        color=["Normal User", "Bot User"],
        color_discrete_map={
            "Normal User": "#4CAF50",
            "Bot User": "#FF5252"
        }
    )

    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )
    fig_pie.update_layout(
        showlegend=True,
        legend_title="User Type",
        margin=dict(t=30, b=0)
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # =============================
    #       TREND BOT DETECTION
    # =============================
    st.markdown("### 📈 Xu hướng số lượng Bot phát hiện theo thời gian (tổng quan)")

    df_bot_detail = load_bot_details()

    bot_trend = (
        df_bot_detail.groupby("detected_date")
        .agg(bot_count=("userID", "nunique"))
        .reset_index()
    )

    fig_line = px.line(
        bot_trend,
        x="detected_date",
        y="bot_count",
        title="Số lượng Bot được phát hiện theo ngày",
        line_shape="spline",
        markers=True,
        template="plotly_dark"
    )

    fig_line.update_traces(
        line=dict(width=2, color="#4287f5"),
        marker=dict(size=5)
    )

    fig_line.update_layout(
        xaxis_title="Ngày",
        yaxis_title="Số lượng Bot",
        xaxis=dict(tickformat="%b %d"),
        hovermode="x unified",
        height=400
    )
    
    st.plotly_chart(fig_line, use_container_width=True)
        # =============================
    #  📊 TREND KHỐI LƯỢNG GIAO DỊCH USER THƯỜNG
    # =============================
    st.markdown("### 🏦 Xu hướng khối lượng giao dịch của người dùng bình thường theo thời gian")

    # Load giao dịch
    df_txn = pd.read_csv("../cleaned_data/transaction_clean.csv")
    df_txn["reqDate"] = pd.to_datetime(df_txn["reqDate"])

    # Merge với tập người dùng để lọc non-bot
    df_txn = df_txn.merge(df_all[["userID", "isBot"]], on="userID", how="left")

    # Chỉ lấy user thường
    df_normal_txn = df_txn[df_txn["isBot"] == 0]

    # Group theo ngày
    df_normal_daily = (
        df_normal_txn.groupby(df_normal_txn["reqDate"].dt.date)["amount"]
        .sum()
        .reset_index()
    )

    # Vẽ biểu đồ
    fig_normal = px.line(
        df_normal_daily,
        x="reqDate",
        y="amount",
        title="Tổng khối lượng giao dịch người dùng bình thường theo ngày",
        line_shape="spline",
        markers=True,
        template="plotly_dark"
    )

    fig_normal.update_layout(
        xaxis_title="Ngày",
        yaxis_title="Khối lượng giao dịch (VND)",
        hovermode="x unified",
        height=400
    )

    st.plotly_chart(fig_normal, use_container_width=True)

    # =============================
    #   FOOTER SUGGESTION
    # =============================
    st.markdown(
        """
        <div style="margin-top:20px; padding:12px; background-color:#1e3a5c; border-radius:8px;">
            🔍 <b>Xem chi tiết từng Bot User</b> tại mục <b>Chi tiết Bot User</b> ở menu bên trái.
        </div>
        """,
        unsafe_allow_html=True
    )
