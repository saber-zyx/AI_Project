import streamlit as st
import pandas as pd
from data_loader import load_bot_details


def render():
    st.header("📜 Chi tiết Bot User")

    df = load_bot_details().copy()

    # Chuẩn hóa kiểu dữ liệu thời gian
    if "detected_date" in df.columns:
        df["detected_date"] = pd.to_datetime(df["detected_date"])

    # ============================================================
    #               TOP 5 BOT MỚI PHÁT HIỆN
    # ============================================================
    st.subheader("🚨 Bot mới bị phát hiện gần đây")

    if "detected_date" in df.columns:
        latest = (
            df.sort_values("detected_date", ascending=False)
              .head(5)[["userID", "detected_date"]]
        )

        for _, row in latest.iterrows():
            st.info(
                f"🔍 **userID `{row['userID']}`** vừa bị phát hiện bot vào lúc "
                f"**{row['detected_date'].strftime('%Y-%m-%d %H:%M:%S')}**",
                icon="⚠️",
            )
    else:
        st.warning("Không tìm thấy cột detected_date trong dữ liệu!")

    # ============================================================
    #               BUTTON GỬI ĐẾN BỘ PHẬN RỦI RO
    # ============================================================
    st.markdown("### 📨 Gửi báo cáo đến bộ phận rủi ro")

    # Khi bấm nút, Streamlit sẽ rerun và nhánh if này = True đúng 1 lần
    if st.button("Gửi cảnh báo ngay 🚀"):
        st.markdown(
            """
            <div style="
                position: fixed;
                top: 40%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0, 128, 255, 0.95);
                padding: 24px 48px;
                border-radius: 14px;
                color: white;
                font-size: 20px;
                font-weight: 600;
                text-align: center;
                z-index: 9999;
                box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            ">
                ✅ Đã gửi thành công đến bộ phận rủi ro!
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ============================================================
    #               TRA CỨU CHI TIẾT BOT USER
    # ============================================================
    st.subheader("🔎 Tra cứu chi tiết Bot User")

    filter_user = st.text_input("Nhập userID để tìm:")

    df_show = df
    if filter_user:
        df_show = df[df["userID"].astype(str).str.contains(filter_user)]

    st.dataframe(df_show, use_container_width=True)
