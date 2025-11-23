import pandas as pd
from functools import lru_cache
import os

# ===============================
#   AUTO PATH
# ===============================
BASE_DIR = os.path.dirname(__file__)


# ===============================
#   LOAD ALL USERS (BOT + NON-BOT)
# ===============================
@lru_cache(maxsize=5)
def load_all_users():
    file_path = os.path.join(BASE_DIR, "all_users_final.csv")
    df = pd.read_csv(file_path)

    df["detected_date"] = pd.to_datetime(df["detected_date"])
    return df


# ===============================
#   LOAD BOT USERS (pred_label == 1)
# ===============================
@lru_cache(maxsize=5)
def load_bot_user():
    df = load_all_users()
    return df[df["isBot"] == 1].copy()


# ===============================
#   LOAD USER OVERVIEW (mỗi user 1 dòng)
# ===============================
def load_user_overview():
    df = load_all_users()

    user_overview = df.groupby("userID").agg({
        "pred_prob": "max",
        "isBot": "max",
        "total_loss": "sum",
        "total_normal_amount": "sum",
        "detected_date": "max"
    }).reset_index()

    return user_overview


# ===============================
#   LOAD CHI TIẾT BOT USER
# ===============================
def load_bot_details():
    df = load_all_users()
    return df[df["isBot"] == 1].copy()


# ===============================
#   KPI dành cho trang Analytics
# ===============================
def load_bot_summary():
    df = load_bot_user()

    summary = {
        # số bot unique
        "total_bots": df["userID"].nunique(),

        # tổng thiệt hại bot gây ra
        "total_loss": df["total_loss"].sum(),

        # range thời gian hoạt động bot
        "min_detect_date": df["detected_date"].min(),
        "max_detect_date": df["detected_date"].max(),

        # trend theo ngày
        "daily_bot_trend":
            df.groupby(df["detected_date"].dt.date)["userID"].nunique(),

        "daily_loss_trend":
            df.groupby(df["detected_date"].dt.date)["total_loss"].sum(),
    }

    return summary
