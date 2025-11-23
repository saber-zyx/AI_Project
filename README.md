# Bot Detection - ZaloPay

## Mục lục
- [Giới thiệu](#giới-thiệu)
- [Thành viên nhóm](#thành-viên-nhóm)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Hướng dẫn cài đặt](#hướng-dẫn-cài-đặt)
- [Liên kết](#liên-kết)

## Giới thiệu

Dự án phát hiện bot trên nền tảng ZaloPay, sử dụng Machine Learning để phân tích và nhận diện hành vi người dùng bất thường.

## Thành viên nhóm

| Họ tên | MSSV |
|--------|------|
|        |      |
|        |      |
|        |      |

## Cấu trúc thư mục

```
AI_Project-main/
├── requirements.txt              # Danh sách các thư viện Python cần thiết
├── raw/                          # Dữ liệu thô ban đầu
│   └── raw data.txt             # File mô tả dữ liệu gốc
├── cleaned_data/                 # Dữ liệu đã được làm sạch
│   └── cleaned data.txt         # File mô tả dữ liệu đã xử lý
├── feature_set/                  # Tập dữ liệu đặc trưng
│   ├── user_feature_set.csv     # Bộ đặc trưng người dùng
│   └── user_feature_set_label.csv # Bộ đặc trưng có nhãn
├── code/                         # Mã nguồn phân tích và mô hình
│   ├── data_cleaning.ipynb      # Notebook làm sạch dữ liệu
│   ├── eda.ipynb                # Notebook phân tích khám phá dữ liệu (EDA)
│   ├── metrics.ipynb            # Notebook đánh giá các chỉ số
│   └── ml.ipynb                 # Notebook xây dựng mô hình Machine Learning
└── dashboard/                    # Ứng dụng Dashboard trực quan hóa
    ├── app.py                   # File chính khởi chạy dashboard
    ├── data_loader.py           # Module tải và xử lý dữ liệu
    ├── overview.py              # Module trang tổng quan
    ├── bot_analytics.py         # Module phân tích bot
    ├── bot_details.py           # Module chi tiết về bot
    ├── all_users_final.csv      # Dữ liệu tất cả người dùng
    └── bot_user_final.csv       # Dữ liệu người dùng bot
```

### Chi tiết các thư mục chính

#### 📂 **raw/**
Chứa dữ liệu thô chưa qua xử lý từ hệ thống ZaloPay.

#### 📂 **cleaned_data/**
Dữ liệu sau khi được làm sạch, loại bỏ nhiễu và chuẩn hóa.

#### 📂 **feature_set/**
Bộ dữ liệu đặc trưng đã được kỹ thuật hóa (feature engineering), sẵn sàng cho việc huấn luyện mô hình.

#### 📂 **code/**
Chứa các Jupyter Notebook để:
- **data_cleaning.ipynb**: Xử lý và làm sạch dữ liệu thô
- **eda.ipynb**: Phân tích khám phá dữ liệu, trực quan hóa các pattern
- **metrics.ipynb**: Tính toán và đánh giá các metrics quan trọng
- **ml.ipynb**: Xây dựng, huấn luyện và đánh giá mô hình ML

#### 📂 **dashboard/**
Ứng dụng web dashboard được xây dựng bằng Streamlit/Dash để:
- Hiển thị tổng quan dữ liệu
- Trực quan hóa kết quả phát hiện bot
- Phân tích chi tiết hành vi người dùng
- Theo dõi các chỉ số hiệu suất

## Hướng dẫn cài đặt

### Yêu cầu hệ thống
- Python 3.8 trở lên
- pip hoặc conda

### Các bước cài đặt

1. Clone repository:
```bash
git clone https://github.com/your-repo-link
cd AI_Project-main
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

3. Chạy dashboard:
```bash
cd dashboard
streamlit run app.py
```

4. Mở trình duyệt và truy cập địa chỉ được hiển thị trong terminal.

## Liên kết

- **Website nhóm**: [https://your-group-website.com](https://your-group-website.com)
- **Repository**: [https://github.com/your-repo-link](https://github.com/your-repo-link)

---

© 2025 Bot Detection - ZaloPay Project
