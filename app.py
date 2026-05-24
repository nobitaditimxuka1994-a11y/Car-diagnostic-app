import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="MINH KHANG AUTO AI", page_icon="⚡", layout="centered")

# CSS tối ưu cho điện thoại
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
    """Ghi log an toàn, chống lỗi 500 khi mạng 4G yếu"""
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

# --- 3. KHO DỮ LIỆU ---
MASTER_DATA = {
    "VINFAST EV": {
        "P0A78": "Lỗi biến tần (Inverter). Kiểm tra hệ thống làm mát & giắc cắm.",
        "P0B59": "Lỗi cảm biến dòng Pin. Cần reset hệ thống BMS.",
        "LOI SAC": "Lỗi không nhận sạc. Kiểm tra tiếp địa trạm sạc & vệ sinh cổng sạc."
    },
    "TOYOTA/LEXUS": {
        "P0101": "Lỗi cảm biến MAF. Vệ sinh cảm biến & kiểm tra lọc gió.",
        "P0171": "Nghèo xăng (Hỗn hợp loãng). Kiểm tra bơm xăng & hở chân không.",
        "KHOI DEN": "Hiện tượng khói đen: Kiểm tra kim phun đái hoặc cảm biến Oxy."
    }
}

# --- 4. QUẢN LÝ PHIÊN LÀM VIỆC (Ghi nhớ trạng thái đồng ý) ---
if 'confirmed' not in st.session_state:
    st.session_state.confirmed = False

if not st.session_state.confirmed:
    st.title("⚡ MINH KHANG AUTO")
    st.error("### ⚠️ CẢNH BÁO TRÁCH NHIỆM")
    st.write("Phần mềm hỗ trợ kỹ thuật chuyên sâu. Người dùng tự chịu trách nhiệm với mọi thao tác sửa chữa.")
    
    if st.button("TÔI ĐỒNG Ý & BẮT ĐẦU"):
        st.session_state.confirmed = True
        st.rerun()
    st.stop()

# --- 5. GIAO DIỆN TRA CỨU ---
st.title("🧑‍🔧 MINH KHANG AUTO ")

brand = st.selectbox("Dòng xe:", list(MASTER_DATA.keys()))
raw_input = st.text_input("Mã lỗi/Hiện tượng:").upper().strip()

if raw_input:
    db = MASTER_DATA[brand]
    found_key = None
    
    for key in db.keys():
        if raw_input in key or key in raw_input:
            found_key = key
            break
            
    if found_key:
        st.success(f"✅ PHÁT HIỆN: {found_key}")
        st.info(db[found_key])
        track_search(brand, raw_input, found_key, "Thành công ✅")
    else:
        st.error("❌ Chưa có dữ liệu mã này.")
        track_search(brand, raw_input, None, "Thất bại ❌")

# --- 6. ADMIN DASHBOARD (ĐÃ BỎ MẬT KHẨU) ---
st.write("---")
with st.expander("📊 Xem lịch sử tra cứu (Admin)"):
    try:
        # Tải dữ liệu và đảo ngược để xem cái mới nhất lên đầu
        history = conn.read(ttl=0)
        st.dataframe(history.iloc[::-1].head(50), use_container_width=True)
        
        # Nút làm mới dữ liệu nhanh
        if st.button("Làm mới dữ liệu"):
            st.rerun()
    except:
        st.warning("Đang kết nối tới máy chủ dữ liệu...")

st.caption("📱 Hotline: 0963227718 | © 2024 Minh Khang Auto")
