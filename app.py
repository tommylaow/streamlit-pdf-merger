import streamlit as st
from pypdf import PdfWriter
import io

# การตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="PDF Merger - เครื่องมือรวมไฟล์ PDF",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# สไตล์ CSS เพิ่มเติมเพื่อให้ดูพรีเมียมและสวยงาม
st.markdown("""
<style>
    .main {
        background-color: #f9fbfd;
    }
    .stButton>button {
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .file-item {
        background-color: #ffffff;
        padding: 12px 20px;
        border-radius: 8px;
        border: 1px solid #e1e8ed;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .file-name {
        font-weight: 500;
        color: #2c3e50;
        font-size: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ส่วนหัวหลักของเว็บ
st.title("📄 PDF Merger")
st.subheader("เครื่องมือออนไลน์สำหรับรวมไฟล์ PDF ของคุณให้เป็นไฟล์เดียว")
st.write("อัปโหลดไฟล์ PDF จัดเรียงลำดับตามที่ต้องการ และดาวน์โหลดไฟล์ผลลัพธ์ได้ทันที")

st.divider()

# กำหนด Session State สำหรับจัดเก็บไฟล์ PDF ที่จะทำการประมวลผล
if 'pdf_list' not in st.session_state:
    st.session_state['pdf_list'] = []

# ตัวอัปโหลดไฟล์
uploaded_files = st.file_uploader(
    "อัปโหลดไฟล์ PDF ของคุณที่นี่ (เลือกได้หลายไฟล์พร้อมกัน)",
    type=["pdf"],
    accept_multiple_files=True,
    key="pdf_uploader"
)

# ประมวลผลเมื่อมีการอัปโหลดไฟล์ใหม่เข้ามา
if uploaded_files:
    for f in uploaded_files:
        # ตรวจสอบเพื่อไม่ให้ไฟล์ซ้ำกันในรายการ (เช็คจากชื่อและขนาด)
        exists = any(item['name'] == f.name and item['size'] == f.size for item in st.session_state['pdf_list'])
        if not exists:
            # อ่านข้อมูลไฟล์ไว้ในหน่วยความจำ
            file_bytes = f.read()
            st.session_state['pdf_list'].append({
                'name': f.name,
                'size': f.size,
                'content': file_bytes
            })

# ส่วนแสดงผลรายการไฟล์ที่เลือกและจัดการลำดับ
if st.session_state['pdf_list']:
    st.write(f"### 📋 รายการไฟล์ PDF ที่เลือกทั้งหมด ({len(st.session_state['pdf_list'])} ไฟล์)")
    st.write("คุณสามารถจัดเรียงลำดับไฟล์โดยการเลื่อนขึ้น/ลง หรือลบไฟล์ที่ไม่ต้องการออกได้")

    # วนลูปแสดงผลรายการไฟล์และปุ่มควบคุม
    for idx, item in enumerate(st.session_state['pdf_list']):
        col_name, col_up, col_down, col_del = st.columns([6, 1, 1, 1])
        
        with col_name:
            st.markdown(f"""
            <div style="padding: 6px 10px; background-color: #edf2f7; border-radius: 6px; margin: 2px 0; font-size: 14px; font-weight: 500; color: #2d3748; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                📍 {idx + 1}. {item['name']}
            </div>
            """, unsafe_allow_html=True)
            
        with col_up:
            # ปุ่มเลื่อนขึ้น (ยกเว้นไฟล์แรก)
            if idx > 0:
                if st.button("⬆️", key=f"up_{idx}", help="เลื่อนขึ้น"):
                    st.session_state['pdf_list'][idx], st.session_state['pdf_list'][idx - 1] = \
                        st.session_state['pdf_list'][idx - 1], st.session_state['pdf_list'][idx]
                    st.rerun()
            else:
                st.write("")
                
        with col_down:
            # ปุ่มเลื่อนลง (ยกเว้นไฟล์สุดท้าย)
            if idx < len(st.session_state['pdf_list']) - 1:
                if st.button("⬇️", key=f"down_{idx}", help="เลื่อนลง"):
                    st.session_state['pdf_list'][idx], st.session_state['pdf_list'][idx + 1] = \
                        st.session_state['pdf_list'][idx + 1], st.session_state['pdf_list'][idx]
                    st.rerun()
            else:
                st.write("")
                
        with col_del:
            # ปุ่มลบไฟล์
            if st.button("🗑️", key=f"del_{idx}", help="ลบไฟล์"):
                st.session_state['pdf_list'].pop(idx)
                st.rerun()

    # ปุ่มล้างรายการทั้งหมด
    if st.button("🧹 ล้างรายการทั้งหมด", key="clear_all"):
        st.session_state['pdf_list'] = []
        st.rerun()

    st.divider()

    # ตั้งชื่อไฟล์ผลลัพธ์
    output_filename = st.text_input("ตั้งชื่อไฟล์ผลลัพธ์หลังจากรวมแล้ว", value="merged_output.pdf")
    if not output_filename.endswith(".pdf"):
        output_filename += ".pdf"

    # ปุ่มสำหรับทำการรวมไฟล์ PDF
    if st.button("🚀 เริ่มต้นรวมไฟล์ PDF", key="btn_merge", use_container_width=True, type="primary"):
        with st.spinner("กำลังดำเนินการรวมไฟล์ PDF กรุณารอสักครู่..."):
            try:
                merger = PdfWriter()
                for item in st.session_state['pdf_list']:
                    # ใช้ BytesIO ในการอ่าน Content ของไฟล์ในหน่วยความจำ
                    merger.append(io.BytesIO(item['content']))
                
                # เขียนผลลัพธ์ลงในหน่วยความจำ
                output_pdf = io.BytesIO()
                merger.write(output_pdf)
                merger.close()
                output_pdf.seek(0)
                
                st.success("🎉 รวมไฟล์ PDF สำเร็จเรียบร้อยแล้ว!")
                
                # ปุ่มดาวน์โหลดไฟล์
                st.download_button(
                    label="📥 ดาวน์โหลดไฟล์ PDF ที่รวมแล้ว",
                    data=output_pdf,
                    file_name=output_filename,
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดในการรวมไฟล์: {str(e)}")

else:
    st.info("💡 กรุณาเลือกอัปโหลดไฟล์ PDF ด้านบนเพื่อเริ่มต้นใช้งาน")

# Footer ส่วนท้ายหน้าเว็บ
st.divider()
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 12px; padding: 10px 0;">
    พัฒนาด้วย ❤️ โดยใช้ Streamlit & pypdf | สามารถนำโค้ดนี้รันบน Streamlit Community Cloud ได้อย่างสะดวกและรวดเร็ว
</div>
""", unsafe_allow_html=True)
