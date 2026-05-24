import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re
from filelock import FileLock
import streamlit as st

# Cấu hình này giúp ép giao diện về Light Mode và mở rộng bố cục
st.set_page_config(
    page_title="Minh Khang Auto AI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded" # Luôn hiện thanh công cụ bên trái
)

# Thêm CSS để đảm bảo nền luôn trắng và chữ luôn đen
st.markdown(
    """
    <style>
    /* Nền chính của App */
    .stApp {
        background-color: white;
    }
    /* Màu chữ tiêu đề và văn bản */
    h1, h2, h3, p, span {
        color: #1f1f1f !important;
    }
    /* Làm nổi bật khung cảnh báo */
    .stAlert {
        background-color: #f8d7da;
        color: #721c24;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Nội dung app của bạn
st.title("⚡ MINH KHANG AUTO AI")
st.subheader("Hệ thống chẩn đoán lỗi Xăng & Điện chuyên sâu")

st.error("⚠️ CẢNH BÁO: Phần mềm dành cho thợ kỹ thuật. Vui lòng xác nhận trước khi dùng.")

if st.button('TÔI ĐỒNG Ý & CHỊU TRÁCH NHIỆM'):
    st.success("Cảm ơn bạn đã xác nhận!")
    # Hiển thị thêm công cụ ở đây

def track_search(brand, user_input, found_code, status):
    log_file = 'search_history.csv'
    lock_path = log_file + ".lock"
    lock = FileLock(lock_path, timeout=5) 
    
    try:
        with lock:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            new_entry = pd.DataFrame({
                "Thời gian": [now],
                "Dòng xe": [brand],
                "Khách gõ": [user_input],
                "AI nhận diện": [found_code if found_code else "Không rõ"],
                "Kết quả": [status]
            })
            
            if not os.path.isfile(log_file):
                new_entry.to_csv(log_file, index=False, encoding='utf-8-sig')
            else:
                new_entry.to_csv(log_file, mode='a', header=False, index=False, encoding='utf-8-sig')
    except Exception as e:
        st.warning(f"Không thể ghi lịch sử do xung đột mạng: {e}")



# --- 1. CẤU HÌNH GIAO DIỆN & STYLE ---
st.set_page_config(page_title="MINH KHANG AUTO - AI DIAGNOSTIC", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stAppDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .reportview-container .main {color: #ffffff; background-color: #0e1117;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. HÀM AI XỬ LÝ THÔNG MINH ---
def ai_process_input(text):
    text = text.lower().strip()
    # Loại bỏ các từ thừa để AI tập trung vào từ khóa chính
    noise_words = ['xe', 'bị', 'lỗi', 'mã', 'hỏng', 'tại sao', 'cách sửa', 'vấn đề']
    for word in noise_words:
        text = text.replace(word, '')
    return text.strip()

# --- 3. HÀM THEO DÕI LỊCH SỬ (TRACKING) ---
def track_search(brand, user_input, found_code, status):
    log_file = 'search_history.csv'
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    new_entry = pd.DataFrame({
        "Thời gian": [now],
        "Dòng xe": [brand],
        "Khách gõ": [user_input],
        "AI nhận diện": [found_code if found_code else "Không rõ"],
        "Kết quả": [status]
    })
    if not os.path.isfile(log_file):
        new_entry.to_csv(log_file, index=False, encoding='utf-8-sig')
    else:
        new_entry.to_csv(log_file, mode='a', header=False, index=False, encoding='utf-8-sig')

# --- 4. KHO DỮ LIỆU LỖI TỔNG HỢP (XĂNG & ĐIỆN) ---
MASTER_DATA = {
    "XE ĐIỆN (VINFAST/EV)": {
        "P0A78": "Lỗi biến tần (Inverter). \n- Kiểm tra hệ thống làm mát cao áp.\n- Kiểm tra giắc cắm lỏng.",
        "P0B59": "Lỗi cảm biến dòng điện Pin. \n- Kiểm tra cáp cao áp.\n- Cần reset hệ thống quản lý Pin (BMS).",
        "LOI SAC": "Lỗi không nhận sạc/Sạc chậm: \n- Kiểm tra súng sạc.\n- Kiểm tra tiếp địa trạm sạc.\n- Vệ sinh cổng sạc trên xe.",
        "PIN YEU": "Pin sụt nhanh: \n- Kiểm tra độ chai Pin (SOH).\n- Cập nhật phần mềm mới nhất cho BMS.",
        "HE THONG LANH": "Điều hòa không mát (Xe điện): \n- Kiểm tra lốc lạnh điện (Electric Compressor).\n- Kiểm tra gas lạnh R1234yf."
    },
    "TOYOTA/LEXUS": {
        "P0101": "Lỗi cảm biến MAF (Khí nạp). \n- Vệ sinh cảm biến bằng dung dịch chuyên dụng.\n- Kiểm tra lọc gió.",
        "P0171": "Nghèo xăng (Hỗn hợp quá loãng). \n- Kiểm tra áp suất bơm xăng.\n- Kiểm tra hở chân không sau bướm ga.",
        "P0300": "Bỏ máy ngẫu nhiên. \n- Kiểm tra hệ thống bugi và bô-bin.\n- Kiểm tra chất lượng xăng.",
        "KHOI DEN": "Khói đen nhiều: \n- Kiểm tra kim phun có bị rò rỉ.\n- Kiểm tra cảm biến Oxy số 1.",
        "KHOI TRANG": "Khói trắng: \n- Kiểm tra nước làm mát có lọt vào buồng đốt (thổi gioăng mặt máy)."
    }
}

# --- 5. GIAO DIỆN CHÍNH ---
st.title("⚡ MINH KHANG AUTO AI")
st.subheader("Hệ thống chẩn đoán lỗi Xăng & Điện chuyên sâu")

# Cảnh báo trách nhiệm
if 'confirmed' not in st.session_state:
    st.error("⚠️ CẢNH BÁO: Phần mềm dành cho thợ kỹ thuật. Vui lòng xác nhận trước khi dùng.")
    if st.button("TÔI ĐỒNG Ý & CHỊU TRÁCH NHIỆM"):
        st.session_state.confirmed = True
        st.rerun()
    st.stop()

# Form nhập liệu
col1, col2 = st.columns([1, 2])
with col1:
    category = st.selectbox("Dòng xe:", list(MASTER_DATA.keys()))
with col2:
    raw_input = st.text_input("Nhập mã lỗi hoặc hiện tượng (Ví dụ: P0A78, lỗi sạc, 171...)")

if raw_input:
    clean_input = ai_process_input(raw_input)
    db = MASTER_DATA[category]
    found_key = None
    
    # AI Search Logic
    for key in db.keys():
        if clean_input in key.lower() or key.lower() in clean_input:
            found_key = key
            break
            
    if found_key:
        st.success(f"✅ AI PHÁT HIỆN: {found_key}")
        st.write(db[found_key])
        track_search(category, raw_input, found_key, "Thành công ✅")
    else:
        st.error("❌ AI chưa có dữ liệu chính xác cho mã này.")
        track_search(category, raw_input, None, "Thất bại ❌")
        st.info("Hệ thống đã ghi lại lỗi này để cập nhật sớm nhất.")

# --- 6. ADMIN DASHBOARD (THEO DÕI LỊCH SỬ) ---
st.write("---")
with st.expander("📊 XEM LỊCH SỬ TÌM KIẾM (CHỈ DÀNH CHO ADMIN)"):
    if os.path.isfile('search_history.csv'):
        history_df = pd.read_csv('search_history.csv')
        st.table(history_df.tail(10)) # Hiển thị 10 lượt gần nhất
        
        # Nút xóa lịch sử nếu cần
        if st.button("Xóa lịch sử"):
            os.remove('search_history.csv')
            st.rerun()
    else:
        st.write("Chưa có dữ liệu tìm kiếm nào.")

# --- 7. FOOTER ---
st.write("---")
st.success("**Kỹ thuật chuyên sâu: Minh Khang Auto**")
st.markdown("#### 📱 Hotline: **0963227718**")
st.caption("Cập nhật liên tục lỗi xe điện VinFast e34, VF8, VF9 và xe xăng đời mới.")
