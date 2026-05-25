import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Cấu hình & Kết nối
st.set_page_config(page_title="MINH KHANG AUTO", layout="centered")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Hàm ghi dữ liệu (Tự động)
def save_log(brand, query, res, status):
    try:
        df = conn.read(ttl=0)
        new_row = pd.DataFrame([{
            "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Dòng xe": brand,
            "Khách gõ": query,
            "AI nhận diện": query,
            "Kết quả": f"{status}: {res}"
        }])
        # Kết hợp và đẩy lên Sheets
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(data=updated_df)
    except:
        pass

# 3. Giao diện tra cứu
st.title("🧑‍🔧 MINH KHANG AUTO AI")

DATA = {
    "VINFAST": {"P0A78": "Lỗi Inverter. Kiểm tra làm mát.", "LOI SAC": "Kiểm tra tiếp địa."},
    "TOYOTA": {"P0101": "Lỗi MAF. Vệ sinh cảm biến.", "P0171": "Nghèo xăng."}
}

brand = st.selectbox("Chọn hãng:", list(DATA.keys()))
query = st.text_input("Nhập mã lỗi/Hiện tượng:").upper().strip()

if query:
    # Cơ chế chống ghi trùng khi load lại trang
    if "old_q" not in st.session_state or st.session_state.old_q != query:
        res = DATA.get(brand, {}).get(query)
        if res:
            st.success(f"✅ KQ: {res}")
            save_log(brand, query, res, "Thành công")
        else:
            st.warning("⚠️ Chưa có mã này.")
            save_log(brand, query, "N/A", "Chưa có mã")
        
        st.session_state.old_q = query

# 4. Xem lịch sử (Dùng bảng đơn giản)
st.write("---")
if st.button("📊 Tải lại nhật ký"):
    try:
        st.dataframe(conn.read(ttl=0).iloc[::-1], use_container_width=True)
    except:
        st.write("Đang kết nối Sheets...")
