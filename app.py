import streamlit as st
from pypdf import PdfWriter, PdfReader
import io
import zipfile

# การตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="PDF Magic Toolkit - เครื่องมือจัดการไฟล์ PDF ครบวงจร",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# สไตล์ CSS เพื่อความสวยงามพรีเมียม
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 16px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        color: #1e293b !important;
    }
    .stButton>button {
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .card-info {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# ส่วนหัวหลัก
st.title("📄 PDF Magic Toolkit")
st.subheader("เครื่องมือจัดการและแก้ไขไฟล์ PDF ครบวงจรบนเว็บของคุณ")
st.write("เลือกเครื่องมือด้านล่างเพื่อจัดการไฟล์ PDF ได้อย่างสะดวกรวดเร็ว")

# แยกเมนูการใช้งานเป็น 3 แท็บหลัก
tab_merge, tab_insert, tab_extract = st.tabs([
    "🔗 รวมไฟล์ปกติ (Merge)", 
    "➕ แทรกหน้าเฉพาะเจาะจง (Insert Pages)", 
    "✂️ แยก/ตัดหน้า PDF (Extract Pages)"
])

# ----------------- TAB 1: รวมไฟล์ปกติ -----------------
with tab_merge:
    st.write("### 🔗 รวมไฟล์ PDF หลายไฟล์")
    st.write("อัปโหลดไฟล์ PDF จัดเรียงลำดับ และทำการรวมเป็นไฟล์เดียวทันที")
    
    if 'pdf_list' not in st.session_state:
        st.session_state['pdf_list'] = []

    # ตัวอัปโหลดไฟล์
    uploaded_files = st.file_uploader(
        "อัปโหลดไฟล์ PDF ของคุณที่นี่ (เลือกได้หลายไฟล์พร้อมกัน)",
        type=["pdf"],
        accept_multiple_files=True,
        key="pdf_uploader"
    )

    if uploaded_files:
        for f in uploaded_files:
            exists = any(item['name'] == f.name and item['size'] == f.size for item in st.session_state['pdf_list'])
            if not exists:
                file_bytes = f.read()
                st.session_state['pdf_list'].append({
                    'name': f.name,
                    'size': f.size,
                    'content': file_bytes
                })

    if st.session_state['pdf_list']:
        st.write(f"#### 📋 รายการไฟล์ในระบบ ({len(st.session_state['pdf_list'])} ไฟล์)")
        
        for idx, item in enumerate(st.session_state['pdf_list']):
            col_name, col_up, col_down, col_del = st.columns([6, 1, 1, 1])
            
            with col_name:
                st.markdown(f"""
                <div style="padding: 6px 10px; background-color: #f1f5f9; border-radius: 6px; margin: 2px 0; font-size: 14px; font-weight: 500; color: #334155; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    📍 {idx + 1}. {item['name']}
                </div>
                """, unsafe_allow_html=True)
                
            with col_up:
                if idx > 0:
                    if st.button("⬆️", key=f"up_{idx}", help="เลื่อนขึ้น"):
                        st.session_state['pdf_list'][idx], st.session_state['pdf_list'][idx - 1] = \
                            st.session_state['pdf_list'][idx - 1], st.session_state['pdf_list'][idx]
                        st.rerun()
                    
            with col_down:
                if idx < len(st.session_state['pdf_list']) - 1:
                    if st.button("⬇️", key=f"down_{idx}", help="เลื่อนลง"):
                        st.session_state['pdf_list'][idx], st.session_state['pdf_list'][idx + 1] = \
                            st.session_state['pdf_list'][idx + 1], st.session_state['pdf_list'][idx]
                        st.rerun()
                    
            with col_del:
                if st.button("🗑️", key=f"del_{idx}", help="ลบไฟล์"):
                    st.session_state['pdf_list'].pop(idx)
                    st.rerun()

        if st.button("🧹 ล้างรายการทั้งหมด", key="clear_all"):
            st.session_state['pdf_list'] = []
            st.rerun()

        st.divider()

        output_filename = st.text_input("ตั้งชื่อไฟล์ผลลัพธ์หลังจากรวมแล้ว", value="merged_output.pdf", key="merge_filename")
        if not output_filename.endswith(".pdf"):
            output_filename += ".pdf"

        if st.button("🚀 เริ่มต้นรวมไฟล์ PDF", key="btn_merge", use_container_width=True, type="primary"):
            with st.spinner("กำลังดำเนินการรวมไฟล์ PDF..."):
                try:
                    writer = PdfWriter()
                    for item in st.session_state['pdf_list']:
                        writer.append(io.BytesIO(item['content']))
                    
                    output_pdf = io.BytesIO()
                    writer.write(output_pdf)
                    writer.close()
                    output_pdf.seek(0)
                    
                    st.success("🎉 รวมไฟล์ PDF สำเร็จเรียบร้อยแล้ว!")
                    st.download_button(
                        label="📥 ดาวน์โหลดไฟล์ PDF ที่รวมแล้ว",
                        data=output_pdf,
                        file_name=output_filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {str(e)}")
    else:
        st.info("💡 กรุณาเลือกอัปโหลดไฟล์ PDF ด้านบนเพื่อเริ่มต้นใช้งาน")


# ----------------- TAB 2: แทรกหน้าเฉพาะเจาะจง -----------------
with tab_insert:
    st.write("### ➕ แทรกหน้าจากชุด A เข้าไปในชุด B")
    st.write("อัปโหลดไฟล์หลัก (B) และไฟล์ต้นทาง (A) เพื่อเลือกดึงบางหน้าจาก A ไปแทรกในตำแหน่งต่างๆ ของ B")
    
    col1, col2 = st.columns(2)
    
    with col1:
        file_b = st.file_uploader("1. เลือกไฟล์หลัก (ชุด B)", type=["pdf"], key="upload_b")
    with col2:
        file_a = st.file_uploader("2. เลือกไฟล์ที่จะนำหน้ามาแทรก (ชุด A)", type=["pdf"], key="upload_a")
        
    if file_b and file_a:
        try:
            reader_b = PdfReader(file_b)
            reader_a = PdfReader(file_a)
            
            pages_b = len(reader_b.pages)
            pages_a = len(reader_a.pages)
            
            st.info(f"📋 ข้อมูลไฟล์: **ชุด B (หลัก)** มี {pages_b} หน้า | **ชุด A (ต้นทาง)** มี {pages_a} หน้า")
            
            st.write("#### ⚙️ ตั้งค่าการแทรกหน้า")
            
            # ให้ผู้ใช้เลือกหน้าจากชุด A
            selected_pages_a = st.multiselect(
                "เลือกเลขหน้าจาก ชุด A ที่ต้องการนำไปแทรก (เลือกได้มากกว่า 1 หน้า)",
                options=list(range(1, pages_a + 1)),
                default=[1]
            )
            
            # เลือกตำแหน่งที่จะวางในชุด B
            insert_position = st.selectbox(
                "ตำแหน่งในชุด B ที่ต้องการนำหน้าจากชุด A ไปแทรก",
                ["แทรกหน้าแรกสุด (ก่อนหน้า 1)", "แทรกท้ายไฟล์ (ต่อท้ายสุด)", "ระบุตำแหน่งเฉพาะเจาะจง"]
            )
            
            target_index = 0
            if insert_position == "แทรกหน้าแรกสุด (ก่อนหน้า 1)":
                target_index = 0
            elif insert_position == "แทรกท้ายไฟล์ (ต่อท้ายสุด)":
                target_index = pages_b
            else:
                target_index = st.number_input(
                    f"แทรกหลังหน้าที่เท่าไหร่ของชุด B (สามารถระบุได้ตั้งแต่หน้า 1 ถึง {pages_b})",
                    min_value=1,
                    max_value=pages_b,
                    value=1
                )
                
            insert_filename = st.text_input("ตั้งชื่อไฟล์รวมใหม่", value="inserted_output.pdf", key="insert_filename")
            if not insert_filename.endswith(".pdf"):
                insert_filename += ".pdf"
                
            if st.button("🚀 ประมวลผลแทรกหน้าและรวมไฟล์", type="primary", use_container_width=True):
                if not selected_pages_a:
                    st.warning("⚠️ กรุณาเลือกเลขหน้าจากชุด A อย่างน้อย 1 หน้า")
                else:
                    with st.spinner("กำลังทำการแทรกและประมวลผล PDF..."):
                        writer = PdfWriter()
                        
                        # 1. ใส่หน้าของชุด B ก่อนถึงจุดแทรก
                        for i in range(target_index):
                            writer.add_page(reader_b.pages[i])
                            
                        # 2. ใส่หน้าที่ดึงมาจากชุด A
                        for p_num in selected_pages_a:
                            writer.add_page(reader_a.pages[p_num - 1])
                            
                        # 3. ใส่หน้าของชุด B ที่เหลืออยู่ทั้งหมด
                        for i in range(target_index, pages_b):
                            writer.add_page(reader_b.pages[i])
                            
                        output_bytes = io.BytesIO()
                        writer.write(output_bytes)
                        writer.close()
                        output_bytes.seek(0)
                        
                        st.success("🎉 ประมวลผลและแทรกหน้าสำเร็จเรียบร้อย!")
                        st.download_button(
                            label="📥 ดาวน์โหลดไฟล์ที่รวมสำเร็จ",
                            data=output_bytes,
                            file_name=insert_filename,
                            mime="application/pdf",
                            use_container_width=True
                        )
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการประมวลผลไฟล์: {str(e)}")
    else:
        st.info("💡 กรุณาอัปโหลดไฟล์ PDF ทั้งชุด B และ ชุด A เพื่อตั้งค่าแทรกหน้า")


# ----------------- TAB 3: แยก/ตัดหน้า PDF -----------------
with tab_extract:
    st.write("### ✂️ แยก/ตัดหน้า PDF ออกเป็นไฟล์ใหม่")
    st.write("อัปโหลดไฟล์ PDF เพื่อแยกออกเป็นไฟล์เดี่ยว หรือตัดช่วงหน้าที่คุณระบุแยกออกมาเป็นหลายๆ ไฟล์")
    
    file_extract = st.file_uploader("เลือกไฟล์ PDF ที่ต้องการแยกหน้า", type=["pdf"], key="upload_extract")
    
    if file_extract:
        try:
            reader_extract = PdfReader(file_extract)
            total_pages = len(reader_extract.pages)
            
            st.info(f"📋 ข้อมูลไฟล์: มีจำนวนทั้งหมด **{total_pages} หน้า**")
            
            st.write("#### ⚙️ ตัวเลือกการแยกหน้า")
            
            extract_mode = st.radio(
                "รูปแบบการแยกหน้า",
                ["แยกช่วงหน้าเป็นหลายๆ ไฟล์ (Multi-file Split)", "ดึงเฉพาะบางหน้ามาสร้างไฟล์ใหม่ไฟล์เดียว (Single-file Extract)"]
            )
            
            if extract_mode == "แยกช่วงหน้าเป็นหลายๆ ไฟล์ (Multi-file Split)":
                st.write("ระบุรูปแบบที่ต้องการแบ่งช่วงหน้า เช่น `1-2, 3-5` ระบบจะทำการสร้างไฟล์ PDF แยกให้ 2 ไฟล์ตามช่วงหน้าดังกล่าว")
                range_input = st.text_input("ระบุช่วงเลขหน้า (คั่นด้วยเครื่องหมายจุลภาค `,`)", value="1-2, 3-5")
                
                if st.button("🚀 ประมวลผลแยกเป็นหลายไฟล์", type="primary", use_container_width=True):
                    # ฟังชั่นการแกะช่วงข้อความเลขหน้า เช่น "1-2, 3-5"
                    splits = []
                    error_found = False
                    for item in range_input.split(","):
                        item = item.strip()
                        if not item:
                            continue
                        if "-" in item:
                            parts = item.split("-")
                            if len(parts) == 2:
                                try:
                                    start = int(parts[0])
                                    end = int(parts[1])
                                    if 1 <= start <= total_pages and 1 <= end <= total_pages:
                                        splits.append((start, end, f"pages_{start}_to_{end}.pdf"))
                                    else:
                                        st.error(f"❌ หน้าที่ระบุ {item} เกินจำนวนหน้าทั้งหมดที่มี ({total_pages} หน้า)")
                                        error_found = True
                                except ValueError:
                                    st.error(f"❌ รูปแบบช่วงหน้าไม่ถูกต้อง: {item}")
                                    error_found = True
                        else:
                            try:
                                val = int(item)
                                if 1 <= val <= total_pages:
                                    splits.append((val, val, f"page_{val}.pdf"))
                                else:
                                    st.error(f"❌ หน้าที่ระบุ {item} เกินจำนวนหน้าทั้งหมดที่มี ({total_pages} หน้า)")
                                    error_found = True
                            except ValueError:
                                st.error(f"❌ รูปแบบเลขหน้าไม่ถูกต้อง: {item}")
                                error_found = True
                                
                    if not error_found and splits:
                        # สร้างไฟล์ ZIP เพื่อรวมไฟล์ทั้งหมดให้ดาวน์โหลดง่ายๆ
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                            for start, end, filename in splits:
                                writer = PdfWriter()
                                for idx in range(start - 1, end):
                                    writer.add_page(reader_extract.pages[idx])
                                pdf_buffer = io.BytesIO()
                                writer.write(pdf_buffer)
                                writer.close()
                                zip_file.writestr(filename, pdf_buffer.getvalue())
                                
                        zip_buffer.seek(0)
                        
                        st.success(f"🎉 แยกไฟล์เรียบร้อยแล้วทั้งหมด {len(splits)} ส่วน!")
                        st.download_button(
                            label="📥 ดาวน์โหลดไฟล์ทั้งหมด (รูปแบบ .ZIP)",
                            data=zip_buffer,
                            file_name="extracted_files.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                        
            else:
                # ดึงเฉพาะบางหน้าเป็นไฟล์เดียว
                selected_pages = st.multiselect(
                    "เลือกเลขหน้าที่ต้องการดึงมารวมกันเป็นไฟล์ใหม่",
                    options=list(range(1, total_pages + 1)),
                    default=[1]
                )
                
                extract_filename = st.text_input("ตั้งชื่อไฟล์แยกหน้าใหม่", value="extracted_output.pdf")
                if not extract_filename.endswith(".pdf"):
                    extract_filename += ".pdf"
                    
                if st.button("🚀 ดึงหน้าและสร้างไฟล์", type="primary", use_container_width=True):
                    if not selected_pages:
                        st.warning("⚠️ กรุณาเลือกหน้าอย่างน้อย 1 หน้า")
                    else:
                        with st.spinner("กำลังดำเนินการดึงหน้า..."):
                            writer = PdfWriter()
                            for p_num in selected_pages:
                                writer.add_page(reader_extract.pages[p_num - 1])
                            
                            output_bytes = io.BytesIO()
                            writer.write(output_bytes)
                            writer.close()
                            output_bytes.seek(0)
                            
                            st.success("🎉 ดึงบางหน้าออกเป็นไฟล์ใหม่สำเร็จแล้ว!")
                            st.download_button(
                                label="📥 ดาวน์โหลดไฟล์ PDF ที่ดึงสำเร็จ",
                                data=output_bytes,
                                file_name=extract_filename,
                                mime="application/pdf",
                                use_container_width=True
                            )
                            
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการวิเคราะห์ไฟล์: {str(e)}")
    else:
        st.info("💡 กรุณาอัปโหลดไฟล์ PDF เพื่อทำการตัด/แยกหน้าไฟล์")

# Footer ส่วนท้ายหน้าเว็บ
st.divider()
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 12px; padding: 10px 0;">
    พัฒนาด้วย ❤️ โดยใช้ Streamlit & pypdf | ลากวางไฟล์ขึ้น GitHub แล้วรันผ่านระบบออนไลน์ได้ทันที
</div>
""", unsafe_allow_html=True)
