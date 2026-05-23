import streamlit as st

# 1. Cấu hình giao diện ẩn Menu
st.set_page_config(page_title="MINH KHANG AUTO", page_icon="🚗")
hide_style = """
    <style>
    .stAppDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# 2. Dữ liệu mã lỗi (Đã sửa lỗi thụt lề)
diagnostic_data = {
    "P0100": "Lỗi mạch lưu lượng khí nạp (MAF). Kiểm tra: Giắc cắm MAF, dây dẫn hoặc hở cổ hút.",
    "P0101": "Hiệu suất mạch MAF không hợp lý. Kiểm tra: Cảm biến bẩn, lọc gió tắc hoặc rò rỉ khí nạp.",
    "P0102": "Mạch MAF có điện áp thấp. Kiểm tra: Cảm biến hỏng hoặc đứt dây nguồn 5V/12V.",
    "P0103": "Mạch MAF có điện áp cao. Kiểm tra: Chạm chập dây tín hiệu hoặc lỗi cảm biến.",
    "P0105": "Lỗi mạch áp suất tuyệt đối cổ hút (MAP). Kiểm tra: Đường ống chân không, cảm biến MAP.",
    "P0110": "Lỗi cảm biến nhiệt độ khí nạp (IAT). Kiểm tra: Vệ sinh cảm biến hoặc kiểm tra giắc cắm.",
    "P0115": "Lỗi mạch nhiệt độ nước làm mát (ECT). Kiểm tra: Cảm biến ECT hỏng hoặc thiếu nước làm mát.",
    "P0116": "Hiệu suất mạch ECT không ổn định. Kiểm tra: Van hằng nhiệt bị kẹt hoặc cảm biến lỗi.",
    "P0120": "Lỗi mạch cảm biến vị trí bướm ga (TPS). Kiểm tra: Cảm biến TPS hoặc họng ga điện.",
    "P0300": "Lỗi bỏ lửa ngẫu nhiên. Kiểm tra: Bugi, bô bin, chất lượng xăng.",
    "P0335": "Lỗi cảm biến vị trí trục khuỷu (CKP). Kiểm tra: Dây điện cảm biến hoặc vành răng xung.",
    "P0420": "Hiệu suất bầu xúc tác thấp. Kiểm tra: Bầu lọc khí thải bị tắc hoặc hỏng.",
    "P0500": "Lỗi cảm biến tốc độ xe (VSS). Kiểm tra: Cảm biến ở hộp số hoặc hệ thống ABS.",
    "khói đen": "Xe bị thừa xăng. Kiểm tra: Cảm biến oxy, kim phun bị đái, hoặc lọc gió quá bẩn.",
    "khói trắng": "Nước làm mát lọt vào buồng đốt. Kiểm tra: Gioăng mặt máy hoặc Turbo.",
}

# 3. Giao diện App
st.title("🚗 MINH KHANG AUTO")
st.write("---")
st.subheader("Tra cứu mã lỗi Toyota nhanh")

# Ô nhập mã lỗi
user_input = st.text_input("Nhập mã lỗi hoặc hiện tượng (VD: P0101, khói đen):")

if user_input:
    # Tìm kiếm không phân biệt chữ hoa chữ thường
    result = diagnostic_data.get(user_input.upper()) or diagnostic_data.get(user_input.lower())
    
    if result:
        st.success(f"**Kết quả:** {result}")
    else:
        st.warning("Không tìm thấy mã lỗi này. Vui lòng kiểm tra lại hoặc liên hệ kỹ thuật.")

st.write("---")
st.info("Phần mềm dành riêng cho thợ chuyên nghiệp Gara Minh Khang.")
