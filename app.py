import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Giao diện tối ưu cho điện thoại
st.set_page_config(page_title="MINH KHANG AUTO AI", layout="centered")
st.markdown("<style>.stAppDeployButton {display: none;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

# 2. Kết nối Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def track_search(brand, user_input, found_code, status):
    try:
        # Lấy dữ liệu cũ
        df = conn.read(ttl=0)
        # Thêm dòng mới
        new_row = pd.DataFrame([{
            "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Dòng xe": brand,
            "Khách gõ": user_input,
            "AI nhận diện": found_code if found_code else "Không rõ",
            "Kết quả": status
        }])
        # Cập nhật ngược lại Sheet
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(data=updated_df)
    except:
        pass # Chống lỗi 500 nếu mạng 4G yếu

# 3. Ghi nhớ trạng thái đồng ý (Chỉ hỏi 1 lần)
if 'confirmed' not in st.session_state:
    st.session_state.confirmed = False

if not st.session_state.confirmed:
    st.error("### ⚠️ CẢNH BÁO: CHỈ DÀNH CHO THỢ CHUYÊN NGHIỆP")
    if st.button("TÔI ĐỒNG Ý & VÀO TRA CỨU"):
        st.session_state.confirmed = True
        st.rerun()
    st.stop()

# 4. Giao diện tra cứu
st.title("🧑‍🔧 MINH KHANG AUTO AI")
MASTER_DATA = {
    "VINFAST EV": {"P0A78": "Lỗi Inverter. Kiểm tra hệ thống làm mát.", "LOI SAC": "Kiểm tra cổng sạc & tiếp địa."},
    "TOYOTA/LEXUS": {"P0101": "Lỗi MAF. Vệ sinh cảm biến nạp.", "P0171": "Nghèo xăng. Kiểm tra bơm xăng."}
}

brand = st.selectbox("Chọn dòng xe:", list(MASTER_DATA.keys()))
raw_input = st.text_input("Nhập mã lỗi:").upper().strip()

if raw_input:
    db = MASTER_DATA[brand]
    res = db.get(raw_input)
    if res:
        st.success(f"✅ KQ: {res}")
        track_search(brand, raw_input, raw_input, "Thành công ✅")
    else:
        st.error("Chưa có dữ liệu.")
        track_search(brand, raw_input, None, "Không thấy ❌")

# 5. Xem lịch sử ngay trong App (Đã bỏ pass)
st.write("---")
with st.expander("📊 Xem lịch sử tra cứu"):
    try:
        history = conn.read(ttl=0)
        st.dataframe(history.iloc[::-1], use_container_width=True)
    except:
        st.write("Đang tải dữ liệu từ Google Sheets...")
