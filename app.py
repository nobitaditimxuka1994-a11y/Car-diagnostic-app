import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Cấu hình giao diện cực gọn cho điện thoại
st.set_page_config(page_title="MINH KHANG AUTO", layout="centered")
st.markdown("<style>.stAppDeployButton {display: none;} header {visibility: hidden;} footer {visibility: hidden;}</style>", unsafe_allow_html=True)

# 2. Thiết lập kết nối
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Cấu hình Secrets chưa đúng. Vui lòng kiểm tra lại link Sheets.")

def save_to_sheets(brand, query, result):
    """Ghi dữ liệu âm thầm, nếu lỗi không làm treo app"""
    try:
        df = conn.read(ttl=0)
        new_row = pd.DataFrame([{
            "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Dòng xe": brand,
            "Khách gõ": query,
            "AI nhận diện": query,
            "Kết quả": result
        }])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(data=updated_df)
    except:
        pass # Lỗi mạng hoặc link Sheets sai sẽ bị bỏ qua tại đây

# 3. Giao diện chính
st.title("🧑‍🔧 MINH KHANG AUTO AI")

# Kho dữ liệu mã lỗi
ERROR_CODES = {
    "VINFAST EV": {
        "P0A78": "Lỗi Biến tần (Inverter). Kiểm tra giắc cam, nước làm mát & vệ sinh giắc cắm.",
        "LOI SAC": "Lỗi không nhận sạc. Kiểm tra súng sạc, tiếp địa hoặc reset bộ sạc treo tường."
    },
    "TOYOTA/LEXUS": {
        "P0101": "Lỗi MAF (Cảm biến gió). Vệ sinh cảm biến và kiểm tra lọc gió bẩn.",
        "P0171": "Hệ thống nhiên liệu quá nghèo. Kiểm tra bơm xăng, kim phun hoặc hở cổ hút."
    }
}

brand = st.selectbox("Chọn dòng xe:", list(ERROR_CODES.keys()))
user_input = st.text_input("Nhập mã lỗi/Hiện tượng:").upper().strip()

if user_input:
    # Ưu tiên hiển thị kết quả trước cho thợ
    db = ERROR_CODES.get(brand, {})
    res = db.get(user_input)
    
    if res:
        st.success(f"🔍 **KẾT QUẢ:** {res}")
        save_to_sheets(brand, user_input, "Thành công")
    else:
        st.warning("Hệ thống chưa cập nhật mã này. Đã ghi nhận để kỹ thuật viên kiểm tra.")
        save_to_sheets(brand, user_input, "Chưa có mã")

# 4. Khu vực xem lịch sử (Chỉ tải khi cần)
st.write("---")
with st.expander("📊 Xem nhật ký tra cứu"):
    if st.button("Tải dữ liệu"):
        try:
            data = conn.read(ttl=0)
            st.dataframe(data.iloc[::-1], use_container_width=True)
        except:
            st.info("Hiện tại chưa thể kết nối tới Google Sheets để xem lịch sử.")
