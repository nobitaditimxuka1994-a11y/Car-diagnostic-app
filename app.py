import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Cấu hình & Kết nối
st.set_page_config(page_title="MINH KHANG AUTO", layout="centered")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Giao diện tra cứu
st.title("🧑‍🔧 MINH KHANG AUTO AI")

DATA = {
    "VINFAST": {"P0A78": "Lỗi Inverter. Kiểm tra làm mát."},
    "TOYOTA": {"P0101": "Lỗi MAF. Vệ sinh cảm biến."}
}

brand = st.selectbox("Hãng xe:", list(DATA.keys()))
query = st.text_input("Nhập mã lỗi:").upper().strip()

if query:
    # Lấy kết quả
    res = DATA.get(brand, {}).get(query, "Chưa có mã")
    if res != "Chưa có mã":
        st.success(f"✅ {res}")
    else:
        st.warning("⚠️ Hệ thống chưa có mã này.")

    # CƯỠNG ÉP GHI DỮ LIỆU (Chạy mỗi khi nhập xong)
    if st.button("XÁC NHẬN LƯU LỊCH SỬ"):
        try:
            # Đọc bảng hiện tại
            df = conn.read(ttl=0)
            # Tạo dòng mới
            new_row = pd.DataFrame([{
                "Thời gian": datetime.now().strftime("%H:%M %d/%m"),
                "Dòng xe": brand,
                "Khách gõ": query,
                "AI nhận diện": query,
                "Kết quả": res
            }])
            # Ghi đè bảng mới
            if df is not None:
                df = pd.concat([df, new_row], ignore_index=True)
            else:
                df = new_row
            
            conn.update(data=df)
            st.balloons() # Hiện hiệu ứng để biết đã lưu xong
            st.success("Đã lưu thành công vào Sheets!")
        except Exception as e:
            st.error(f"Lỗi: {e}")

# 3. Xem lịch sử
st.write("---")
if st.button("📊 Tải lại bảng"):
    st.dataframe(conn.read(ttl=0).iloc[::-1], use_container_width=True)
