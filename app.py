import streamlit as st
# --- CODE ẨN MENU VÀ GITHUB ---
st.set_page_config(page_title="MINH KHANG AUTO", page_icon="🚗", layout="centered")

hide_style = """
    <style>
    /* Ẩn nút GitHub, Fork và nút 3 chấm ở góc trên phải */
    .stAppDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .viewerBadge_container__1QS1n {display: none;}
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)


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
DIAGNOSTIC_KEYWORDS = {
        # NHÓM CẢM BIẾN KHÍ NẠP & NHIÊN LIỆU (01-10)
        "P0100": "Lỗi mạch lưu lượng khí nạp (MAF). Kiểm tra: Giắc cắm MAF, dây dẫn hoặc hở cổ hút.",
        "P0101": "Hiệu suất mạch MAF không hợp lý. Kiểm tra: Cảm biến bẩn, lọc gió tắc hoặc rò rỉ khí nạp.",
        "P0102": "Mạch MAF có điện áp thấp. Kiểm tra: Cảm biến hỏng hoặc đứt dây nguồn 5V/12V.",
        "P0103": "Mạch MAF có điện áp cao. Kiểm tra: Chạm chập dây tín hiệu hoặc lỗi cảm biến.",
        "P0105": "Lỗi mạch áp suất tuyệt đối cổ hút (MAP). Kiểm tra: Đường ống chân không, cảm biến MAP.",
        "P0110": "Lỗi cảm biến nhiệt độ khí nạp (IAT). Kiểm tra: Vệ sinh cảm biến hoặc kiểm tra giắc cắm.",
        "P0115": "Lỗi mạch nhiệt độ nước làm mát (ECT). Kiểm tra: Cảm biến ECT hỏng hoặc thiếu nước làm mát.",
        "P0116": "Hiệu suất mạch ECT không ổn định. Kiểm tra: Van hằng nhiệt bị kẹt hoặc cảm biến lỗi.",
        "P0120": "Lỗi mạch cảm biến vị trí bướm ga (TPS) - Nhánh A. Kiểm tra: Cảm biến TPS hoặc họng ga điện.",
        "P0121": "Hiệu suất cảm biến bướm ga không hợp lý. Kiểm tra: Vệ sinh họng ga, kiểm tra độ rơ bướm ga.",

        # NHÓM CẢM BIẾN OXY & TỈ LỆ A/F (11-30)
        "P0130": "Lỗi mạch cảm biến Oxy (Bank 1 Sensor 1). Kiểm tra: Dây dẫn cảm biến hoặc lỗi chính cảm biến.",
        "P0133": "Cảm biến Oxy phản ứng chậm (Bank 1 Sensor 1). Kiểm tra: Cảm biến bị đóng muội than quá nhiều.",
        "P0134": "Mạch cảm biến Oxy không hoạt động (Bank 1 Sensor 1). Kiểm tra: Đứt dây sấy cảm biến.",
        "P0136": "Lỗi mạch cảm biến Oxy (Bank 1 Sensor 2). Kiểm tra: Cảm biến sau bầu xúc tác.",
        "P0171": "Hệ thống nhiên liệu quá nghèo (Bank 1). Kiểm tra: Lọc xăng, bơm xăng yếu, rò rỉ khí nạp.",
        "P0172": "Hệ thống nhiên liệu quá giàu (Bank 1). Kiểm tra: Kim phun đái, cảm biến MAF sai số, lọc gió bẩn.",
        "P0174": "Hệ thống nhiên liệu quá nghèo (Bank 2). Thường gặp trên máy V6 (Camry, Prado).",
        "P0175": "Hệ thống nhiên liệu quá giàu (Bank 2). Kiểm tra: Hệ thống phun xăng nhánh 2.",

        # NHÓM ĐÁNH LỬA & BỎ LỬA (31-50)
        "P0300": "Lỗi bỏ lửa ngẫu nhiên (Multiple Misfire). Kiểm tra: Bugi, bô bin, chất lượng nhiên liệu.",
        "P0301": "Bỏ lửa xi lanh số 1. Kiểm tra: Hoán đổi bô bin số 1 sang số 2 để loại trừ.",
        "P0302": "Bỏ lửa xi lanh số 2. Kiểm tra: Bugi hoặc kim phun số 2.",
        "P0303": "Bỏ lửa xi lanh số 3. Kiểm tra: Bô bin hoặc nén xi lanh.",
        "P0304": "Bỏ lửa xi lanh số 4. Kiểm tra: Bugi hoặc đường dây điện bô bin.",
        "P0325": "Lỗi cảm biến kích nổ (Knock Sensor 1). Kiểm tra: Chuột cắn dây điện dưới gầm máy.",
        "P0327": "Điện áp cảm biến kích nổ thấp. Kiểm tra: Lỏng giắc cảm biến.",
        "P0330": "Lỗi cảm biến kích nổ 2 (Bank 2). Kiểm tra: Cảm biến nhánh số 2.",
        "P0335": "Lỗi mạch cảm biến vị trí trục khuỷu (CKP). Kiểm tra: Cảm biến hoặc vành răng xung.",
        "P0339": "Mạch cảm biến trục khuỷu chập chờn. Kiểm tra: Giắc cắm lỏng hoặc nhiễu điện.",
        "P0340": "Lỗi mạch cảm biến vị trí trục cam (CMP). Kiểm tra: Cảm biến cam hoặc đặt sai cam.",

        # NHÓM HỆ THỐNG KHÍ THẢI & EVAP (51-70)
        "P0401": "Lưu lượng luân hồi khí thải (EGR) kém. Kiểm tra: Vệ sinh van EGR hoặc đường ống EGR.",
        "P0403": "Lỗi mạch điều khiển van EGR. Kiểm tra: Cuộn dây van EGR hoặc dây dẫn.",
        "P0420": "Hiệu suất bầu xúc tác thấp (Bank 1). Kiểm tra: Bầu Cataytic bị tắc hoặc hỏng.",
        "P0430": "Hiệu suất bầu xúc tác thấp (Bank 2). Kiểm tra: Bầu xúc tác nhánh 2.",
        "P0441": "Lỗi hệ thống kiểm soát hơi xăng (EVAP) - Dòng chảy không chuẩn. Kiểm tra: Bình than hoạt tính.",
        "P0442": "Rò rỉ hệ thống EVAP (Lỗ rò nhỏ). Kiểm tra: Nắp bình xăng hoặc đường ống hơi xăng.",
        "P0455": "Rò rỉ hệ thống EVAP (Lỗ rò lớn). Kiểm tra: Tuột ống hơi xăng hoặc hỏng van xả.",

        # NHÓM ĐIỀU KHIỂN TỐC ĐỘ CẦM CHỪNG & HỆ THỐNG PHỤ (71-100)
        "P0500": "Lỗi cảm biến tốc độ xe (VSS). Kiểm tra: Cảm biến tốc độ đầu ra hộp số hoặc ABS.",
        "P0505": "Lỗi hệ thống điều khiển không tải (ISC/IAC). Kiểm tra: Vệ sinh van không tải hoặc họng ga.",
        "P0511": "Mạch điều khiển khí không tải lỗi. Kiểm tra: Dây điện van không tải.",
        "P0560": "Điện áp hệ thống không bình thường. Kiểm tra: Bình ắc quy hoặc máy phát điện (Dinamo).",
        "P0601": "Lỗi bộ nhớ trong hộp điều khiển (ECM/PCM). Cách xử lý: Cài đặt lại phần mềm hoặc thay hộp.",
        "P0606": "Lỗi bộ xử lý ECM/PCM. Kiểm tra: Nguồn hộp hoặc thay hộp mới.",
        "P0705": "Lỗi mạch cảm biến dải số (Công tắc rẻ quạt). Kiểm tra: Vị trí cần số và giắc cắm hộp số.",
        "P0741": "Lỗi ly hợp biến mô (Lock-up) luôn ngắt. Kiểm tra: Dầu hộp số hoặc van Solenoid TCC.",
        "P0850": "Mạch công tắc trung gian P/N lỗi. Kiểm tra: Không cho đề nổ ở số D.",
        "P0973": "Lỗi Solenoid chuyển số A - Điện áp thấp. Kiểm tra: Cuộn dây solenoid trong hộp số.",
        "P2118": "Lỗi dòng điện motor bướm ga. Kiểm tra: Cầu chì ETCS 10A trong khoang máy.",
        "P2195": "Cảm biến A/F bị kẹt nghèo (Bank 1 Sensor 1). Kiểm tra: Thay cảm biến A/F đầu lốc máy.",
        
        # Bổ sung một số hiện tượng Toyota hay gặp
        "mất bù ga": "Thường do bẩn họng ga hoặc hỏng van không tải. Xử lý: Vệ sinh họng ga và cài đặt lại (Reset).",
        "đạp ga không lên": "Kiểm tra chế độ an toàn (Limp Mode), thường do lỗi họng ga điện hoặc cảm biến bàn đạp ga.",
        "rung giật khi dừng đèn đỏ": "Kiểm tra cao su chân máy hoặc bỏ lửa nhẹ xi lanh.",
        "vô lăng bị lệch": "Kiểm tra thước lái hoặc cân bằng động, chỉnh lại góc đặt bánh xe."
    

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
