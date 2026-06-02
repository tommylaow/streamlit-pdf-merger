# PDF Merger Web App (Streamlit)

แอปพลิเคชันบนเว็บที่มีหน้าตาการใช้งานสวยงาม พัฒนาด้วยภาษา Python และ Streamlit สำหรับใช้รวมไฟล์ PDF หลายๆ ไฟล์เข้าด้วยกัน โดยผู้ใช้สามารถปรับลำดับการจัดวางของไฟล์ก่อนรวมและลบไฟล์ที่ไม่ต้องการออกได้ตามต้องการ

## 🚀 วิธีการรันโปรแกรมในเครื่องคอมพิวเตอร์ของคุณ (Local)

1. **ติดตั้งไลบรารีที่จำเป็น**
   เปิด Command Prompt หรือ PowerShell ในโฟลเดอร์นี้ แล้วรันคำสั่ง:
   ```bash
   pip install -r requirements.txt
   ```

2. **สั่งรันแอปพลิเคชัน Streamlit**
   ใช้คำสั่งด้านล่างเพื่อเปิดทดสอบใช้งานผ่านหน้าเว็บในเครื่องคอมพิวเตอร์ของคุณ:
   ```bash
   streamlit run app.py
   ```

---

## 🌐 วิธีนำขึ้น GitHub และเชื่อมต่อเข้ากับ Streamlit Cloud

หากคุณต้องการให้แอปพลิเคชันนี้ทำงานออนไลน์ได้ตลอดเวลาเพื่อให้ผู अदอื่นเข้ามาใช้งานได้ด้วย ให้ทำตามขั้นตอนดังนี้:

### ขั้นตอนที่ 1: อัปโหลดโปรเจกต์นี้ขึ้น GitHub
1. เปิด Git Bash หรือ Terminal ในโฟลเดอร์นี้
2. เริ่มต้นระบบ Git และทำ Commit แรก:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Streamlit PDF Merger"
   ```
3. สร้าง Repository ใหม่บน [GitHub](https://github.com/) ของคุณ (ตั้งชื่อเช่น `streamlit-pdf-merger`)
4. เชื่อมโยง Git ในเครื่องของคุณกับ GitHub และทำการ Push โค้ดขึ้นไป:
   ```bash
   git branch -M main
   git remote add origin https://github.com/ชื่อผู้ใช้ของคุณ/ชื่อเรโพสิทอรีของคุณ.git
   git push -u origin main
   ```

### ขั้นตอนที่ 2: ตั้งค่าใช้งานบน Streamlit Community Cloud
1. ไปที่เว็บไซต์ [Streamlit Community Cloud](https://share.streamlit.io/) และเข้าสู่ระบบด้วยบัญชี GitHub ของคุณ
2. คลิกปุ่ม **"Create app"** หรือ **"Deploy an app"**
3. กรอกรายละเอียดดังนี้:
   - **Repository:** เลือก Repository GitHub ของคุณที่เพิ่ง Push โค้ดขึ้นไป
   - **Branch:** เลือก `main`
   - **Main file path:** พิมพ์คำว่า `app.py`
4. คลิกปุ่ม **"Deploy!"**
5. รอระบบติดตั้ง Environment ประมาณ 1-2 นาที คุณจะได้ URL เว็บไซต์พร้อมใช้งานทันที!
