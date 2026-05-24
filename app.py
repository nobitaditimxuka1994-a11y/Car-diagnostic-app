import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="MINH KHANG AUTO ", page_icon="⚡", layout="centered")

# Ẩn menu thừa để app gọn hơn trên điện thoại
st.markdown("""<style>
    .stAppDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>""", unsafe_allow_html=True)

# --- 2. KẾT NỐI GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def track_search(brand, user_input, found_code, status):
    """Ghi lịch sử vào Google Sheets, bỏ qua nếu lỗi mạng"""
    try:
        # Đọc data cũ
        df = conn.read(ttl=0)
        # Tạo dòng mới
        new_row = pd.DataFrame([{
            "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Dòng xe": brand,
            "Khách gõ": user_input,
            "AI nhận diện": found_code if found_code else "Không rõ",
            "Kết quả": status
        }])
        # Ghi đè lên Sheets
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(data=updated_df)
    except:
        # Nếu 4G yếu quá không ghi được thì "im lặng" để app không sập
        pass

# --- 3. KHO DỮ LIỆU (Bạn có thể thêm mã lỗi ở đây) ---
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

# --- 4. GIAO DIỆN CHÍNH ---
st.title("⚡ MINH KHANG AUTO AI")

# Xác nhận trách nhiệm
if 'confirmed' not in st.session_state:
    st.error("⚠️ PHẦN MỀM DÀNH CHO THỢ CHUYÊN NGHIỆP")
    if st.button("TÔI ĐỒNG Ý & VÀO TRA CỨU"):
        st.session_state.confirmed = True
        st.rerun()
    st.stop()

# Form nhập liệu
brand = st.selectbox("Chọn dòng xe:", list(MASTER_DATA.keys()))
raw_input = st.text_input("Nhập mã lỗi hoặc hiện tượng:").upper().strip()

if raw_input:
    db = MASTER_DATA[brand]
    found_key = None
    
    # Tìm kiếm (khớp chính xác hoặc chứa từ khóa)
    for key in db.keys():
        if raw_input in key or key in raw_input:
            found_key = key
            break
            
    if found_key:
        st.success(f"✅ KẾT QUẢ: {found_key}")
        st.write(db[found_key])
        track_search(brand, raw_input, found_key, "Thành công ✅")
    else:
        st.error("❌ Chưa có dữ liệu mã này.")
        track_search(brand, raw_input, None, "Thất bại ❌")

# --- 5. ADMIN DASHBOARD (Xem lịch sử) ---
st.write("---")
with st.expander("📊 Lịch sử tra cứu"):
    admin_pass = st.text_input("Mật khẩu Admin:", type="password")
    if admin_pass == "0963227718": # Thay đổi mật khẩu của bạn tại đây
        try:
            history_df = conn.read(ttl=0)
            st.dataframe(history_df.tail(20), use_container_width=True)
        except:
            st.warning("Đang kết nối dữ liệu...")

# --- 6. LIÊN HỆ ---
st.info("📞 Hotline kỹ thuật: 0963227718")
