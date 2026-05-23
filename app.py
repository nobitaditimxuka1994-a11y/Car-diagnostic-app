import streamlit as st

# 1. Cấu hình giao diện và ẩn Menu thừa
st.set_page_config(page_title="MINH KHANG AUTO", page_icon="🚗", layout="centered")

hide_style = """
    <style>
    .stAppDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# --- PHẦN 1: CẢNH BÁO ĐỎ (Hiện ngay khi mở App) ---
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
    st.stop() # Dừng app tại đây nếu chưa bấm đồng ý

# --- PHẦN 2: GIAO DIỆN CHÍNH (Sau khi đã đồng ý) ---
st.title("🚗 MINH KHANG AUTO")
st.markdown("#### Hệ thống Tra cứu Mã lỗi & Kỹ thuật Sửa chữa")

# 3. CHỌN HÃNG XE
brand = st.selectbox("Chọn hãng xe:", ["Toyota", "Lexus", "Hãng khác (Đang cập nhật)"])

# 4. DỮ LIỆU CHI TIẾT (Bạn có thể dán thêm 100 mã lỗi vào đây)
toyota_data = {
    "P0101": """**Lỗi:** Hiệu suất mạch MAF.
**Cách xử lý:** 1. Vệ sinh cảm biến MAF. 2. Kiểm tra lọc gió. 3. Kiểm tra rò rỉ khí nạp.""",
    "P0171": """**Lỗi:** Hệ thống nhiên liệu quá nghèo.
**Cách xử lý:** 1. Kiểm tra áp suất bơm xăng. 2. Kiểm tra kim phun. 3. Kiểm tra hở chân không.""",
    "khói đen": """**Hiện tượng:** Xe ra khói đen.
**Kiểm tra:** 1. Lọc gió bẩn. 2. Kim phun đái. 3. Cảm biến Oxy hỏng.""",
}

# 5. LOGIC TRA CỨU
if brand == "Toyota":
    user_input = st.text_input("Nhập mã lỗi Toyota (VD: P0101):").upper().strip()
    if user_input:
        if user_input in toyota_data:
            st.info(f"🔍 **KẾT QUẢ CHO MÃ: {user_input}**")
            st.write(toyota_data[user_input])
        else:
            st.error("Chưa có dữ liệu cho mã này. Hãy gọi cho Nhà phát triển bên dưới.")

# --- PHẦN 6: THÔNG TIN NHÀ PHÁT TRIỂN (Số điện thoại của bạn) ---
st.write("---")
st.markdown("### 📞 HỖ TRỢ KỸ THUẬT")
st.success("**Nhà phát triển:** Chủ Gara Minh Khang")
# HÃY THAY SỐ ĐIỆN THOẠI CỦA BẠN VÀO DÒNG DƯỚI ĐÂY
st.markdown("#### 📱 Hotline: **0963227718**") 
st.caption("© 2024 Gara Minh Khang Auto - Kỹ thuật chuyên sâu")
