import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="MINH KHANG AUTO AI", page_icon="⚡", layout="centered")

# Style để ẩn menu và làm gọn giao diện điện thoại
st.markdown("""<style>
    .stAppDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>""", unsafe_allow_html=True)

# --- 2. KẾT NỐI GOOGLE SHEETS ---
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

# --- 3. KHO DỮ LIỆU ---
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

# --- 4. LOGIC XÁC NHẬN (FIX LỖI BẤT TIỆN) ---
# Sử dụng session_state để app nhớ là đã đồng ý rồi
if 'confirmed' not in st.session_state:
    st.session_state.confirmed = False

if not st.session_state.confirmed:
    st.warning("### ⚠️ CẢNH BÁO BẮT BUỘC")
    st.write("Phần mềm dành cho thợ chuyên nghiệp. Mọi hậu quả khi làm sai kỹ thuật bạn phải tự chịu trách nhiệm.")
    if st.button("TÔI ĐỒNG Ý & BẮT ĐẦU"):
        st.session_state.confirmed = True
        st.rerun() # Chạy lại app để vào thẳng mục tra cứu
    st.stop() # Dừng tất cả code phía dưới cho đến khi nhấn nút

# --- 5. GIAO DIỆN TRA CỨU (Chỉ hiện khi đã confirmed = True) ---
st.title("⚡ MINH KHANG AUTO AI")

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
        st.success(f"✅ KẾT QUẢ: {found_key}")
        st.write(db[found_key])
        track_search(brand, raw_input, found_key, "Thành công ✅")
    else:
        st.error("❌ Chưa có dữ liệu mã này.")
        track_search(brand, raw_input, None, "Thất bại ❌")

# --- 6. ADMIN DASHBOARD (FIX LỖI BẢO MẬT PASS) ---
st.write("---")
with st.expander("📊 Xem lịch sử tra cứu"):
    admin_pass = st.text_input("Mật khẩu Admin:", type="password", key="admin_pwd")
    
    # Chỉ khi mật khẩu khớp mới thực hiện lệnh đọc Sheets và hiện bảng
    if admin_pass == "0963227718": 
        try:
            history_df = conn.read(ttl=0)
            st.success("Xác thực thành công!")
            st.dataframe(history_df.iloc[::-1].head(20), use_container_width=True) 
        except:
            st.error("Lỗi kết nối dữ liệu Sheets.")
    elif admin_pass != "":
        st.error("Mật khẩu không đúng!")

st.info("📞 Hotline kỹ thuật: 0963227718")
