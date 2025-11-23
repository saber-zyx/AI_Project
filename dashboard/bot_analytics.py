# bot_analytics.py
import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import load_bot_user


def render():
    st.title("🤖 Phân tích hành vi Bot User")

    # -------------------------------------------------
    #              LOAD DATA
    # -------------------------------------------------
    df = load_bot_user().copy()

    df["detected_date"] = pd.to_datetime(df["detected_date"])

    # -------------------------------------------------
    #              SIDEBAR FILTER
    # -------------------------------------------------
    st.sidebar.subheader("🔎 Bộ lọc")

    min_date = df["detected_date"].min()
    max_date = df["detected_date"].max()

    date_range = st.sidebar.date_input(
        "Khoảng thời gian phát hiện Bot",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )

    promotion_types = sorted(df["promotion_type"].dropna().unique())
    selected_promo = st.sidebar.multiselect(
        "Loại khuyến mãi",
        promotion_types,
        default=promotion_types
    )

    df_filtered = df[
        (df["detected_date"] >= pd.to_datetime(date_range[0])) &
        (df["detected_date"] <= pd.to_datetime(date_range[1])) &
        (df["promotion_type"].isin(selected_promo))
    ].copy()

    if df_filtered.empty:
        st.warning("❗ Không có dữ liệu phù hợp bộ lọc.")
        return

    st.markdown("---")

    # -------------------------------------------------
    #     1. TREND BOT & LOSS THEO THỜI GIAN
    # -------------------------------------------------
    st.subheader("📅 Xu hướng phát hiện Bot & thiệt hại theo thời gian")

    df_daily = (
        df_filtered.groupby("detected_date")
        .agg(
            bot_count=("userID", "nunique"),
            total_loss=("total_loss", "sum"),
        )
        .reset_index()
    )

    col1, col2 = st.columns(2)

    # ---- Trend bot theo ngày ----
    with col1:
        fig_bot = px.line(
            df_daily,
            x="detected_date",
            y="bot_count",
            markers=True,
            title="Số lượng Bot theo ngày",
            template="plotly_white"
        )
        fig_bot.update_layout(height=350, xaxis_tickangle=-45)
        st.plotly_chart(fig_bot, use_container_width=True)

    # ---- Trend loss theo ngày ----
    with col2:
        fig_loss = px.line(
            df_daily,
            x="detected_date",
            y="total_loss",
            markers=True,
            title="Tổng thiệt hại theo ngày",
            template="plotly_white"
        )
        fig_loss.update_layout(height=350, xaxis_tickangle=-45)
        st.plotly_chart(fig_loss, use_container_width=True)

    st.markdown("---")

    # -------------------------------------------------
    #     2. TOP 5 CHIẾN DỊCH BỊ ẢNH HƯỞNG
    # -------------------------------------------------
    st.subheader("🔥 Top 5 chiến dịch bị ảnh hưởng nặng nhất bởi Bot")

    if "campaignName" in df_filtered.columns:
        campaign_col = "promotionName"
    else:
        campaign_col = "campaignCode"

    top_campaigns = (
        df_filtered.groupby([campaign_col, "promotion_type"])["userID"]
        .nunique()
        .reset_index(name="bot_count")
        .sort_values("bot_count", ascending=False)
        .head(5)
    )

    fig_top5 = px.bar(
        top_campaigns,
        x="bot_count",
        y=campaign_col,
        orientation="h",
        color="promotion_type",
        text="bot_count",
        title="Top 5 Campaign bị Bot tấn công nhiều nhất",
        template="plotly_white",
    )

    fig_top5.update_traces(textposition="outside")
    fig_top5.update_layout(
        yaxis_title="Tên Campaign",
        xaxis_title="Số lượng Bot",
        height=450,
        margin=dict(l=20, r=20, t=80, b=20),
    )

    st.plotly_chart(fig_top5, use_container_width=True)
    st.markdown("---")

    # -------------------------------------------------
    #       3. BOT THEO LOẠI KHUYẾN MÃI
    # -------------------------------------------------
    st.subheader("🎯 Phân bố Bot theo loại khuyến mãi")

    df_promo = (
        df_filtered.groupby("promotion_type")
        .agg(
            bot_count=("userID", "nunique"),
            total_loss=("total_loss", "sum"),
        )
        .reset_index()
    )

    colp1, colp2 = st.columns(2)

    # ---- Bot count theo loại khuyến mãi ----
    with colp1:
        fig_cnt = px.bar(
            df_promo,
            x="promotion_type",
            y="bot_count",
            text="bot_count",
            title="Số lượng Bot theo loại khuyến mãi",
            template="plotly_white"
        )
        fig_cnt.update_traces(textposition="outside")
        fig_cnt.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=80, b=20),
            xaxis_tickangle=-30
        )
        st.plotly_chart(fig_cnt, use_container_width=True)

    # ---- Loss theo loại khuyến mãi ----
    with colp2:
        fig_loss_promo = px.bar(
            df_promo,
            x="promotion_type",
            y="total_loss",
            text="total_loss",
            title="Tổng thiệt hại theo loại khuyến mãi",
            template="plotly_white"
        )
        fig_loss_promo.update_traces(textposition="outside")
        fig_loss_promo.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=80, b=20),
            xaxis_tickangle=-30
        )
        st.plotly_chart(fig_loss_promo, use_container_width=True)

    st.success("🎯 Dashboard Bot User đã sẵn sàng vận hành!")
