import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="MINH KHANG AUTO AI", page_icon="⚡", layout="centered")

st.markdown("""<style>
    .stAppDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stButton button {width: 100%; border-radius: 10px; height: 50px; font-weight: bold;}
</style>""", unsafe_allow_html=True)

# --- 2. KẾT NỐI GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def track_search(brand, user_input, found_code, status):
    """Ghi log trực tiếp vào Google Sheets"""
    try:
        # Đọc dữ liệu hiện có
        df = conn.read(ttl=0)
        # Tạo dòng dữ liệu mới
        new_row = pd.DataFrame([{
            "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Dòng xe": brand,
            "Khách gõ": user_input,
            "AI nhận diện": found_code if found_code else "Không rõ",
            "Kết quả": status
        }])
        # Cập nhật bảng
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(data=updated_df)
    except Exception as e:
        # Nếu lỗi mạng 4G, app vẫn chạy bình thường
        pass 

# --- 3. DỮ LIỆU MÃ LỖI ---
MASTER_DATA = {
    "VINFAST EV": {
        "P0A78": "Lỗi biến tần (Inverter). Kiểm tra làm mát & giắc cắm.",
        "P0B59": "Lỗi cảm biến dòng Pin. Cần reset BMS.",
        "LOI SAC": "Lỗi không nhận sạc. Kiểm tra tiếp địa & cổng sạc."
    },
    "TOYOTA/LEXUS": {
        "P0101": "Lỗi cảm biến MAF. Vệ sinh cảm biến & lọc gió.",
        "P0171": "Nghèo xăng. Kiểm tra bơm xăng & hở chân không.",
        "KHOI DEN": "Kiểm tra kim phun & cảm biến Oxy."
    }
}

# --- 4. XÁC NHẬN SỬ DỤNG (Lưu trạng thái bằng Session State) ---
if 'confirmed' not in st.session_state:
    st.session_state.confirmed = False

if not st.session_state.confirmed:
    st.title("⚡ MINH KHANG AUTO")
    st.error("### ⚠️ CẢNH BÁO TRÁCH NHIỆM")
    st.write("Phần mềm dành cho thợ chuyên nghiệp. Bạn tự chịu trách nhiệm với mọi thao tác sửa chữa.")
    if st.button("TÔI ĐỒNG Ý & VÀO TRA CỨU"):
        st.session_state.confirmed = True
        st.rerun()
    st.stop()

# --- 5. GIAO DIỆN TRA CỨU ---
st.title("🧑‍🔧 MINH KHANG AUTO AI")

brand = st.selectbox("Chọn dòng xe:", list(MASTER_DATA.keys()))
raw_input = st.text_input("Nhập mã lỗi hoặc hiện tượng:").upper().strip()

if raw_input:
    db = MASTER_DATA[brand]
    found_key = None
    for key in db.keys():
        if raw_input in key or key in raw_input:
            found_key = key
            break
            
    if found_key:
        st.success(f"✅ KQ: {found_key}")
        st.info(db[found_key])
        track_search(brand, raw_input, found_key, "Thành công ✅")
    else:
        st.error("❌ Chưa có dữ liệu.")
        track_search(brand, raw_input, None, "Thất bại ❌")

# --- 6. XEM LỊCH SỬ (ADMIN) ---
st.write("---")
with st.expander("📊 Xem lịch sử tra cứu (Admin)"):
    try:
        history = conn.read(ttl=0)
        st.dataframe(history.iloc[::-1].head(50), use_container_width=True)
    except:
        st.warning("Đang kết nối dữ liệu...")

st.caption("📱 Hotline: 0963227718")
