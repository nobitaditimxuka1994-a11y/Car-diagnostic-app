import streamlit as st
import pandas as pd
from datetime import datetime
import os
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="MINH KHANG AUTO", page_icon="🧑‍🔧", layout="centered")

# --- HÀM AI XỬ LÝ CHUỖI (GIÚP AI THÔNG MINH HƠN) ---
def ai_clean_input(text):
    # Loại bỏ các từ thừa mà thợ hay gõ
    text = text.lower().strip()
    text = re.sub(r'(lỗi|mã|xe|bị|máy|hỏng)', '', text).strip()
    return text.upper()

# --- HÀM THEO DÕI ---
def track_user_search(brand, user_input, result_found):
    log_file = 'search_history.csv'
    now = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    new_data = pd.DataFrame({
        "Thời gian": [now],
        "Hãng xe": [brand],
        "Mã khách nhập": [user_input],
        "Kết quả": ["Tìm thấy ✅" if result_found else "Không thấy ❌"]
    })
    if not os.path.isfile(log_file):
        new_data.to_csv(log_file, index=False, encoding='utf-8-sig')
    else:
        new_data.to_csv(log_file, mode='a', header=False, index=False, encoding='utf-8-sig')

# --- DỮ LIỆU (Nâng cấp thêm nhiều từ khóa để AI dễ tìm) ---
toyota_data = {
    "P0101": "Lỗi cảm biến lưu lượng khí nạp (MAF). \n- Kiểm tra vệ sinh cảm biến.\n- Kiểm tra hở cổ hút.",
    "P0171": "Hỗn hợp nhiên liệu quá nghèo (Nghèo xăng). \n- Kiểm tra bơm xăng.\n- Kiểm tra kim phun.",
    "KHOI DEN": "Hiện tượng khói đen: \n- Kiểm tra lọc gió.\n- Kiểm tra kim phun có bị đái không.\n- Cảm biến oxy.",
    "P0301": "Bỏ máy số 1: \n- Kiểm tra Bugi máy 1.\n- Kiểm tra Bô-bin đánh lửa.",
}

# --- GIAO DIỆN ---
st.title("🧑‍🔧 MINH KHANG AUTO")

if 'agreed' not in st.session_state:
    st.session_state.agreed = False

if not st.session_state.agreed:
    st.warning("Vui lòng xác nhận trách nhiệm kỹ thuật trước khi dùng.")
    if st.button("TÔI ĐỒNG Ý"):
        st.session_state.agreed = True
        st.rerun()
    st.stop()

brand = st.selectbox("Hãng xe:", ["Toyota", "Lexus", "Khác"])
user_raw = st.text_input("Nhập mã lỗi hoặc triệu chứng:").strip()

if user_raw:
    clean_input = ai_clean_input(user_raw) # AI làm sạch dữ liệu gõ sai
    found_key = None

    # Vòng lặp AI tìm kiếm thông minh
    for key in toyota_data.keys():
        if clean_input in key or key in clean_input:
            found_key = key
            break
    
    if found_key:
        st.success(f"🔍 AI PHÁN ĐOÁN: MÃ {found_key}")
        st.write(toyota_data[found_key])
        track_user_search(brand, user_raw, True)
    else:
        st.error("AI không tìm thấy trong dữ liệu hiện tại.")
        track_user_search(brand, user_raw, False)
        st.info("Yêu cầu đã được gửi đến Minh Khang Auto để cập nhật thêm.")

# --- MỤC ADMIN XEM LỊCH SỬ ---
st.write("---")
with st.expander("📂 NHẬT KÝ KHÁCH TÌM KIẾM (ADMIN ONLY)"):
    if os.path.isfile('search_history.csv'):
        df = pd.read_csv('search_history.csv')
        st.table(df.tail(5)) # Hiển thị 5 dòng mới nhất dạng bảng cho dễ nhìn
    else:
        st.write("Chưa có lịch sử nào.")

st.markdown("#### 📱 Hotline: **0963227718**")

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="MINH KHANG AUTO", page_icon="🧑‍🔧", layout="centered")

hide_style = """
    <style>
    .stAppDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# --- PHẦN 1: HÀM THEO DÕI (TRACKING) ---
def track_user_search(brand, user_input, result_found):
    # Tạo file tracking.csv nếu chưa có
    log_file = 'search_history.csv'
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_data = {
        "Thời gian": [now],
        "Hãng xe": [brand],
        "Mã khách nhập": [user_input],
        "Tìm thấy": ["Có" if result_found else "Không"]
    }
    df_new = pd.DataFrame(new_data)
    
    # Ghi vào file (nối thêm dòng mới)
    if not os.path.isfile(log_file):
        df_new.to_csv(log_file, index=False, encoding='utf-8-sig')
    else:
        df_new.to_csv(log_file, mode='a', header=False, index=False, encoding='utf-8-sig')

# --- PHẦN 2: CẢNH BÁO BẮT BUỘC ---
if 'agreed' not in st.session_state:
    st.session_state.agreed = False

if not st.session_state.agreed:
    st.error("""
    ### ⚠️ CẢNH BÁO BẮT BUỘC:
    ĐÂY LÀ PHẦN MỀM DÀNH CHO THỢ SỬA XE CHUYÊN NGHIỆP ĐƯỢC ĐÀO TẠO BÀI BẢN. 
    MỌI HẬU QUẢ KHI LÀM VIỆC SAI NGUYÊN TẮC VÀ KỸ THUẬT SẼ PHẢI TỰ CHỊU TRÁCH NHIỆM!
    """)
    if st.button("TÔI ĐÃ HIỂU VÀ ĐỒNG Ý"):
        st.session_state.agreed = True
        st.rerun()
    st.stop()

# --- PHẦN 3: GIAO DIỆN CHÍNH ---
st.title("🧑‍🔧 MINH KHANG AUTO")
st.markdown("#### Hệ thống Tra cứu AI & Kỹ thuật Sửa chữa")

brand = st.selectbox("Chọn hãng xe:", ["Toyota", "Lexus", "Hãng khác"])

# DỮ LIỆU MÃ LỖI
toyota_data = {
    "P0101": """**Lỗi:** Hiệu suất mạch MAF.\n**Cách xử lý:** 1. Vệ sinh cảm biến MAF. 2. Kiểm tra lọc gió. 3. Kiểm tra rò rỉ khí nạp.""",
    "P0171": """**Lỗi:** Hệ thống nhiên liệu quá nghèo.\n**Cách xử lý:** 1. Kiểm tra áp suất bơm xăng. 2. Kiểm tra kim phun. 3. Kiểm tra hở chân không.""",
    "KHOI DEN": """**Hiện tượng:** Xe ra khói đen.\n**Kiểm tra:** 1. Lọc gió bẩn. 2. Kim phun đái. 3. Cảm biến Oxy hỏng.""",
}

# --- PHẦN 4: LOGIC TRA CỨU AI (GIẢ LẬP) ---
if brand == "Toyota":
    user_input = st.text_input("Nhập mã lỗi hoặc hiện tượng (VD: P0101, khói đen):").strip().upper()
    
    if user_input:
        found_key = None
        
        # AI tìm kiếm gần đúng (nhận diện cả khi khách nhập thiếu chữ P hoặc gõ nhầm)
        for key in toyota_data.keys():
            if user_input in key or key in user_input:
                found_key = key
                break
        
        if found_key:
            st.info(f"🔍 **KẾT QUẢ AI PHÂN TÍCH CHO: {found_key}**")
            st.write(toyota_data[found_key])
            track_user_search(brand, user_input, True) # Lưu tracking thành công
        else:
            st.error("AI chưa tìm thấy mã này trong dữ liệu hệ thống.")
            track_user_search(brand, user_input, False) # Lưu tracking thất bại để bạn biết mà cập nhật
            st.warning("Thông tin đã được gửi tới kỹ thuật viên để cập nhật dữ liệu mới.")

# --- PHẦN 5: DÀNH CHO CHỦ APP (XEM LỊCH SỬ) ---
# Đoạn này bạn có thể ẩn đi hoặc đặt mật khẩu
with st.expander("Admin: Xem lịch sử khách tìm kiếm"):
    if os.path.isfile('search_history.csv'):
        history_df = pd.read_csv('search_history.csv')
        st.dataframe(history_df.tail(10)) # Hiện 10 dòng gần nhất
    else:
        st.write("Chưa có dữ liệu tìm kiếm.")

# --- PHẦN 6: THÔNG TIN LIÊN HỆ ---
st.write("---")
st.markdown("### 📞 HỖ TRỢ KỸ THUẬT")
st.success("**Nhà phát triển:** Minh Khang Auto ")
st.markdown("#### 📱 Hotline: **0963227718**") 
st.caption("© 2024 Minh Khang Auto - Kỹ thuật chuyên sâu")
