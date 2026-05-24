import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Cấu hình giao diện
st.set_page_config(page_title="MINH KHANG AUTO AI", layout="centered")
st.markdown("<style>.stAppDeployButton {display: none;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

# 2. Kết nối Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def track_search(brand, user_input, found_code, status):
    try:
        df = conn.read(ttl=0)
        new_row = pd.DataFrame([{
            "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Dòng xe": brand,
            "Khách gõ": user_input,
            "AI nhận diện": found_code if found_code else "Không rõ",
            "Kết quả": status
        }])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(data=updated_df)
    except:
        pass

# 3. Quản lý trạng thái đồng ý (Session State)
if 'confirmed' not in st.session_state:
    st.session_state.confirmed = False

if not st.session_state.confirmed:
    st.error("### ⚠️ CẢNH BÁO TRÁCH NHIỆM")
    if st.button("TÔI ĐỒNG Ý & VÀO TRA CỨU"):
        st.session_state.confirmed = True
        st.rerun()
    st.stop()

# 4. Giao diện chính
st.title("🧑‍🔧 MINH KHANG AUTO AI")
MASTER_DATA = {
    "VINFAST EV": {"P0A78": "Lỗi Inverter. Kiểm tra làm mát.", "LOI SAC": "Kiểm tra tiếp địa sạc."},
    "TOYOTA": {"P0101": "Lỗi MAF. Vệ sinh cảm biến.", "P0171": "Nghèo xăng."}
}

brand = st.selectbox("Chọn xe:", list(MASTER_DATA.keys()))
raw_input = st.text_input("Nhập mã lỗi:").upper().strip()

if raw_input:
    db = MASTER_DATA[brand]
    res = db.get(raw_input)
    if res:
        st.success(f"✅ KQ: {res}")
        track_search(brand, raw_input, raw_input, "Thành công ✅")
    else:
        st.error("Chưa có dữ liệu.")
        track_search(brand, raw_input, None, "Thất bại ❌")

# 5. Xem lịch sử (Đã bỏ mật khẩu)
st.write("---")
with st.expander("📊 Lịch sử tra cứu"):
    try:
        history = conn.read(ttl=0)
        st.dataframe(history.iloc[::-1], use_container_width=True)
    except:
        st.write("Chưa có dữ liệu.")
