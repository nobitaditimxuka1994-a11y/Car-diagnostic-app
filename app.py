import streamlit as st

# ---------------------------------------------------------
# Cấu hình trang & Giao diện tối chuyên nghiệp cho Mobile
# ---------------------------------------------------------
st.set_page_config(
    page_title="MINH KHANG AUTO",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Thêm CSS custom để giao diện đẹp hơn trên điện thoại
st.markdown("""
    <style>
    .main-title { font-size: 26px !important; color: #00ffcc; text-align: center; font-weight: bold; margin-bottom: 0px; }
    .sub-title { font-size: 14px; color: #ffffff; text-align: center; margin-bottom: 20px; }
    .disclaimer-box { background-color: #ff4d4d; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-weight: bold; text-align: justify; }
    .cause-box { background-color: #ffe6e6; border-left: 5px solid #d9534f; padding: 12px; border-radius: 4px; color: #333; }
    .fix-box { background-color: #e6ffe6; border-left: 5px solid #5cb85c; padding: 12px; border-radius: 4px; color: #333; }
    </style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# DỮ LIỆU CHẨN ĐOÁN
# ---------------------------------------------------------
DIAGNOSTIC_DATA = {
    "Toyota": {
        "P0300": {
            "keywords": ["p0300", "bo lua", "misfire"],
            "cause": "Bỏ lửa ngẫu nhiên nhiều xi-lanh. Do bugi mòn, bô-bin hỏng hoặc kim phun bẩn.",
            "fix": "Kiểm tra và thay thế bugi hoặc bô-bin hỏng. Súc rửa kim phun xăng."
        },
        "P0171": {
            "keywords": ["p0171", "ngheo xang", "lean"],
            "cause": "Hệ thống nhiên liệu quá nghèo (quá nhiều không khí). Do rò rỉ khí nạp hoặc cảm biến MAF bẩn.",
            "fix": "Vệ sinh cảm biến lưu lượng khí nạp (MAF), kiểm tra các đường ống cao su đường nạp xem có hở không."
        },
        "HIEUTUONG_KHOI_DEN": {
            "keywords": ["khoi den", "ra khoi den", "an xang"],
            "cause": "Hỗn hợp hòa khí quá giàu (thừa xăng, thiếu khí). Nguyên nhân do nghẹt lọc gió, hỏng cảm biến oxy, áp suất nhiên liệu quá cao hoặc kim phun bị đái.",
            "fix": "Thay lọc gió động cơ, kiểm tra kim phun, đo áp suất bơm xăng và kiểm tra tín hiệu cảm biến oxy."
        },
        "HIEUTUONG_RUNG_MAY": {
            "keywords": ["rung", "giat", "rung giat", "no may"],
            "cause": "Động cơ bị bỏ máy (misfire), cao su chân máy bị lão hóa/vỡ, hoặc do họng ga bẩn gây sai lệch garanti.",
            "fix": "Kiểm tra xem có máy nào không nổ, kiểm tra cao su chân máy và tiến hành vệ sinh họng ga, van không tải."
        }
    },
    "Honda": {
        "P0420": {
            "keywords": ["p0420", "catalytic", "bau loc"],
            "cause": "Hiệu suất bộ xúc tác khí thải dưới ngưỡng. Do bầu lọc khí thải bị tắc hoặc hỏng cảm biến oxy.",
            "fix": "Kiểm tra cảm biến oxy trước/sau. Nếu cảm biến tốt thì cần vệ sinh hoặc thay bầu xúc tác."
        }
    }
}

def remove_sign(text):
    import re
    text = text.lower()
    text = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', text)
    text = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', text)
    text = re.sub(r'[ìíịỉĩ]', 'i', text)
    text = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', text)
    text = re.sub(r'[ùúụủũưừứựửữ]', 'u', text)
    text = re.sub(r'[ỳýỵỷỹ]', 'y', text)
    text = re.sub(r'[đ]', 'd', text)
    return text

# ---------------------------------------------------------
# QUY TRÌNH HIỂN THỊ (CẢNH BÁO -> MÀN HÌNH CHÀO -> APP CHÍNH)
# ---------------------------------------------------------

# Dùng Session State của Streamlit để quản lý luồng màn hình
if 'step' not in st.session_state:
    st.session_state.step = 'disclaimer'

# BƯỚC 1: CẢNH BÁO TRÁCH NHIỆM
if st.session_state.step == 'disclaimer':
    st.markdown('<div class="disclaimer-box">⚠️ CẢNH BÁO BẮT BUỘC:<br><br>ĐÂY LÀ PHẦN MỀM DÀNH CHO THỢ SỬA XE CHUYÊN NGHIỆP ĐƯỢC ĐÀO TẠO BÀI BẢN. MỌI HẬU QUẢ KHI LÀM VIỆC SAI NGUYÊN TẮC VÀ KỸ THUẬT SẼ PHẢI TỰ CHỊU HẬU QUẢ!</div>', unsafe_allow_html=True)
    if st.button("TÔI ĐÃ HIỂU VÀ ĐỒNG Ý", use_container_width=True):
        st.session_state.step = 'splash'
        st.rerun()

# BƯỚC 2: MÀN HÌNH CHÀO THƯƠNG HIỆU
elif st.session_state.step == 'splash':
    st.markdown('<div class="main-title">MINH KHANG AUTO</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Nhà phát triển: Đội ngũ Minh Khang<br>Hotline hỗ trợ kỹ thuật: 0963227718</div>', unsafe_allow_html=True)
    
    if st.button("VÀO PHẦN MỀM CHẨN ĐOÁN", type="primary", use_container_width=True):
        st.session_state.step = 'main'
        st.rerun()

# BƯỚC 3: GIAO DIỆN CHẨN ĐOÁN CHÍNH
elif st.session_state.step == 'main':
    st.markdown('<h2 style="text-align:center; color:#00ffcc;">HỆ THỐNG CHẨN ĐOÁN THÔNG MINH</h2>', unsafe_allow_html=True)
    st.write(f"**Gara:** MINH KHANG AUTO | **Hotline:** 0963227718")
    st.divider()

    # Chọn hãng xe
    brand = st.selectbox("Chọn hãng xe cần tra cứu:", list(DIAGNOSTIC_DATA.keys()))
    
    # Nhập lỗi
    user_input = st.text_input("Nhập mã lỗi hoặc hiện tượng bệnh của xe:", placeholder="Ví dụ: P0300, khoi den, may rung...")

    if st.button("CHẨN ĐOÁN NGAY", type="primary", use_container_width=True):
        if user_input.strip() == "":
            st.warning("Vui lòng điền mã lỗi hoặc hiện tượng xe!")
        else:
            search_query = remove_sign(user_input)
            brand_data = DIAGNOSTIC_DATA.get(brand, {})
            found_data = None

            for key, details in brand_data.items():
                for keyword in details["keywords"]:
                    if keyword in search_query:
                        found_data = details
                        break
                if found_data: break

            st.divider()
            if found_data:
                st.subheader("🔴 Nguyên nhân có thể xảy ra:")
                st.markdown(f'<div class="cause-box">{found_data["cause"]}</div>', unsafe_allow_html=True)
                
                st.subheader("🟢 Biện pháp / Quy trình khắc phục:")
                st.markdown(f'<div class="fix-box">{found_data["fix"]}</div>', unsafe_allow_html=True)
            else:
                st.error(f"Hệ thống chưa có dữ liệu chính xác cho: '{user_input}'")
                st.info("Mẹo: Hãy thử gõ từ khóa ngắn hơn (ví dụ: 'khói đen', 'rung máy') và đảm bảo chọn đúng hãng xe.")
