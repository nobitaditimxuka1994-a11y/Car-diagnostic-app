import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Cấu hình giao diện tối ưu cho điện thoại
st.set_page_config(page_title="MINH KHANG AUTO AI", layout="centered")
st.markdown("<style>.stAppDeployButton {display: none;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

# 2. Kết nối Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def track_search(brand, user_input, found_code, status):
    """Hàm ghi lịch sử: Tự tạo dữ liệu mới nếu không đọc được Sheets cũ"""
    try:
        # Thử đọc dữ liệu hiện tại, nếu lỗi thì tạo bảng mới hoàn toàn
        try:
            df = conn.read(ttl=0)
        except:
            df = pd.DataFrame(columns=["Thời gian", "Dòng xe", "Khách gõ", "AI nhận diện", "Kết quả"])
        
        # Thêm dòng mới
        new_row = pd.DataFrame([{
            "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Dòng xe": brand,
            "Khách gõ": user_input,
            "AI nhận diện": found_code if found_code else "Không rõ",
            "Kết quả": status
        }])
        
        # Kết hợp và cập nhật
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(data=updated_df)
    except:
        # Đảm bảo app không bao giờ bị treo nếu lỗi mạng
        pass

# 3. Quản lý trạng thái xác nhận
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

# 4. Giao diện tra cứu chính
st.title("🧑‍🔧 MINH KHANG AUTO AI")

MASTER_DATA = {
    "VINFAST EV": {
        "P0A78": "Lỗi Inverter. Kiểm tra hệ thống làm mát & giắc cắm.",
        "LOI SAC": "Kiểm tra tiếp địa trạm sạc & cổng sạc."
    },
    "TOYOTA/LEXUS": {
        "P0101": "Lỗi cảm biến MAF. Vệ sinh cảm biến & lọc gió.",
        "P0171": "Nghèo xăng. Kiểm tra bơm xăng & hở chân không."
    }
}

brand = st.selectbox("Chọn dòng xe:", list(MASTER_DATA.keys()))
raw_input = st.text_input("Nhập mã lỗi:").upper().strip()

if raw_input:
    db = MASTER_DATA[brand]
    res = db.get(raw_input)
    if res:
        st.success(f"✅ KQ: {res}")
        # Chạy ghi log ngầm, không làm gián đoạn người dùng
        track_search(brand, raw_input, raw_input, "Thành công ✅")
    else:
        st.error("Chưa có dữ liệu cho mã lỗi này.")
        track_search(brand, raw_input, None, "Không thấy ❌")

# 5. Xem lịch sử (Sửa lỗi treo app tại đây)
st.write("---")
with st.expander("📊 Xem lịch sử tra cứu"):
    if st.button("Tải dữ liệu mới nhất"):
        try:
            history = conn.read(ttl=0)
            if history.empty:
                st.write("Chưa có dữ liệu lịch sử.")
            else:
                st.dataframe(history.iloc[::-1], use_container_width=True)
        except Exception as e:
            st.warning("Không thể kết nối với Google Sheets. Vui lòng kiểm tra lại cấu hình Secrets.")
            st.info("Lưu ý: Link Sheets trong Secrets phải ở dạng 'spreadsheet = \"link...\"' trên cùng 1 dòng.")
