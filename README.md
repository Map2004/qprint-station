# 🖨️ QPrint Station

> **Smart Document Printing & PromptPay Automated Payment System**  
> เว็บแอปพลิเคชันสำหรับบริการสั่งพิมพ์เอกสารอัตโนมัติพร้อมระบบชำระเงินผ่าน PromptPay QR Code และตรวจสอบสลิปแบบเรียลไทม์

---

## 🌐 Language / ภาษา
- [English](#-english-version)
- [ภาษาไทย](#-ภาษาไทย)

---

## 🇬🇧 English Version

### 📖 Project Title & Description
**QPrint Station** is a full-stack self-service printing web application designed to streamline the document printing workflow. Users can upload PDF documents, preview pages directly in the browser, customize print settings (specific page ranges and color modes), calculate print costs dynamically, and complete payments seamlessly via dynamically generated PromptPay QR codes. The system automatically validates transaction slips using the SlipOK API and queues print jobs with real-time queue tracking.

---

### ✨ Key Features
- **📄 Client-Side PDF Preview & Page Detection**: Interactive first-page PDF preview and total page calculation powered by [PDF.js](https://mozilla.github.io/pdf.js/) before uploading.
- **⚙️ Custom Print Settings**: Flexible page range selection (e.g., `1-3, 7, 9-11`) and color mode selection (Black & White / Full Color).
- **💰 Dynamic Pricing Engine**: Automatic cost calculation based on selected pages and color mode (THB 1/page for B&W, THB 3/page for Color).
- **📱 Dynamic PromptPay QR Code Generation**: Instant QR code generation with exact amounts embedded via PromptPay.
- **🔍 Automated Bank Slip Verification**: Real-time payment verification integrating the **SlipOK API**, confirming transaction legitimacy, timestamps, and reference codes.
- **⏱️ Session Management & Security**: 15-minute transaction session timeouts, secure randomized hex Request IDs (`rid`), thread-safe state management (`threading.Lock`), and server-side file format validation.
- **📊 Real-time Queue Tracking**: Multi-step single-page application (SPA) state flow (Upload ➔ Payment ➔ Queue Status / Error Handling) with live queue checking.

---

### 🛠️ Tech Stack
- **Backend**: Python 3, [Bottle Framework](https://bottlepy.org/) (Micro WSGI Web Framework)
- **WSGI Server**: [Cheroot](https://cheroot.cherrypy.dev/) (High-performance multi-threaded HTTP server)
- **PDF Processing**: `pypdf` (Server-side PDF stream reading & validation)
- **Payment & APIs**: SlipOK API (Bank slip verification), PromptPay.io QR API
- **Frontend**: HTML5, Vanilla CSS3 (Custom Responsive Gradient UI), Vanilla JavaScript (ES6+), PDF.js

---

### 📂 Project Structure
```text
qprint-station/
├── uploads/              # Temporary storage for uploaded PDF documents and slip images
├── views/
│   └── index.html        # Interactive Single Page Application (UI, CSS, JS, PDF.js integration)
├── test.py               # Main application backend, REST APIs, pricing logic, and SlipOK integration
├── .gitignore            # Git ignore configuration (venv, uploads, pycache)
└── README.md             # Project documentation (English & Thai)
```

#### Core Files Description:
- **`test.py`**: The central application entry point. Handles routing, file uploads, in-memory PDF parsing, pricing rules, thread-safe session storage, SlipOK API calls, and printer queue dispatching.
- **`views/index.html`**: The unified frontend SPA containing views for PDF upload/preview, payment instructions, slip submission, error handling, and queue monitoring.

---

### 🚀 Getting Started / Installation

Follow these steps to set up and run the project locally on your machine:

#### 1. Clone the Repository
```bash
git clone https://github.com/Map2004/qprint-station.git
cd qprint-station
```

#### 2. Create and Activate a Python Virtual Environment
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Windows**:
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

#### 3. Install Dependencies
Install all required libraries using `pip`:
```bash
pip install bottle pypdf requests cheroot
```
*(Optional) If using `requirements.txt`:*
```bash
pip install -r requirements.txt
```

#### 4. Run the Server
```bash
python3 test.py
```
After running, open your web browser and navigate to:  
👉 **`http://localhost:8080`**

---

### 💡 Usage Guide
1. **Upload Document**: Select a `.pdf` file. The frontend will render a preview of page 1 and detect total page count.
2. **Configure Print Settings**: Specify target pages (e.g., `1-5`) or leave blank for all pages, then choose Black/White or Color mode. Click **Upload**.
3. **Scan & Pay**: Review the calculated cost and scan the displayed PromptPay QR Code with your banking app.
4. **Submit Slip**: Upload the payment transfer slip (`.png`, `.jpg`, `.jpeg`).
5. **Get Queue Number**: Once verified by SlipOK, your print job will be submitted to the queue and your queue number will be displayed on screen.

---
---

## 🇹🇭 ภาษาไทย

### 📖 ชื่อโครงการและคำอธิบายภาพรวม
**QPrint Station** คือเว็บแอปพลิเคชันให้บริการสั่งพิมพ์เอกสารอัตโนมัติ (Self-Service Printing Station) ออกแบบมาเพื่อยกระดับความสะดวกและลดขั้นตอนการสั่งพิมพ์ ผู้ใช้สามารถอัปโหลดไฟล์เอกสาร PDF, ดูตัวอย่างหน้าเอกสาร (Preview) ได้ทันทีบนเบราว์เซอร์, เลือกหน้าและโหมดสีที่ต้องการพิมพ์, ระบบจะคำนวณราคาอัตโนมัติและสร้าง PromptPay QR Code ตามยอดเงินที่ต้องชำระจริง พร้อมทั้งมีระบบตรวจสอบสลิปโอนเงินอัตโนมัติผ่าน SlipOK API และออกหมายเลขคิวการพิมพ์แบบเรียลไทม์

---

### ✨ ฟีเจอร์หลัก (Key Features)
- **📄 แสดงตัวอย่างเอกสารทันที (Client-Side Preview)**: แสดงผลพรีวิวหน้าแรกของ PDF และตรวจนับจำนวนหน้าทั้งหมดผ่าน [PDF.js](https://mozilla.github.io/pdf.js/) ก่อนส่งข้อมูล
- **⚙️ กำหนดการพิมพ์ได้ตามต้องการ**: รองรับการระบุช่วงหน้า เช่น `1-3, 7, 9-11` และเลือกโหมดสี (ขาวดำ / สี)
- **💰 คำนวณราคาอัตโนมัติ (Dynamic Pricing)**: คิดราคาตามจำนวนหน้าที่เลือกและโหมดสี (ขาวดำ 1 บาท/หน้า, สี 3 บาท/หน้า)
- **📱 สร้าง QR Code พร้อมเพย์ตามยอดจริง**: สร้าง PromptPay QR Code ที่มียอดเงินที่ถูกต้องโดยอัตโนมัติ สะดวกต่อการสแกนจ่าย
- **🔍 ตรวจสอบสลิปโอนเงินอัตโนมัติผ่าน API**: ตรวจเช็คความถูกต้องของสลิปธนาคารแบบเรียลไทม์ด้วย **SlipOK API** ยืนยันรหัสธุรกรรม (Transaction Ref) ป้องกันสลิปปลอม
- **⏱️ ระบบจัดการเซสชันและความปลอดภัย**: กำหนดอายุการทำรายการภายใน 15 นาที, สุ่มรหัส Request ID (`rid`) ที่ปลอดภัย, จัดการข้อมูลแบบ Thread-safe ด้วย `threading.Lock` และตรวจสอบความถูกต้องของไฟล์ฝั่งเซิร์ฟเวอร์
- **📊 ติดตามสถานะคิวการพิมพ์**: รองรับสถานะการทำงานหลายขั้นตอนในหน้าเดียว (SPA) พร้อมปุ่มตรวจสอบคิวการพิมพ์แบบเรียลไทม์

---

### 🛠️ เทคโนโลยีที่ใช้ (Tech Stack)
- **ฝั่งเซิร์ฟเวอร์ (Backend)**: Python 3, [Bottle Framework](https://bottlepy.org/)
- **เว็บเซิร์ฟเวอร์ (WSGI Server)**: [Cheroot](https://cheroot.cherrypy.dev/) (Multi-threaded WSGI server)
- **การจัดการไฟล์ PDF**: `pypdf` (อ่านข้อมูล stream และตรวจสอบความยาวหน้าบน memory)
- **ระบบชำระเงินและ API**: SlipOK API (ตรวจสลิปธนาคาร), PromptPay.io QR API
- **ฝั่งผู้ใช้งาน (Frontend)**: HTML5, Vanilla CSS3 (ดีไซน์ Gradient การ์ดรองรับ Responsive), Vanilla JavaScript (ES6+), PDF.js

---

### 📂 โครงสร้างโปรเจกต์ (Project Structure)
```text
qprint-station/
├── uploads/              # โฟลเดอร์จัดเก็บไฟล์เอกสารและรูปสลิปที่ผู้ใช้อัปโหลด
├── views/
│   └── index.html        # หน้าเว็บหลักแบบ SPA (รวม HTML, CSS, JavaScript และ PDF.js)
├── test.py               # ไฟล์เซิร์ฟเวอร์หลัก, API endpoints, ตรรกะคิดราคา และเชื่อมต่อ SlipOK
├── .gitignore            # กำหนดไฟล์/โฟลเดอร์ที่ไม่นำขึ้น Git (venv, uploads, __pycache__)
└── README.md             # เอกสารอธิบายโปรเจกต์ (ภาษาอังกฤษและภาษาไทย)
```

#### รายละเอียดไฟล์สำคัญ:
- **`test.py`**: ศูนย์กลางการทำงานของระบบฝั่ง Backend ดูแล Routing, รับไฟล์อัปโหลด, ตรวจสอบและนับหน้า PDF, คำนวณค่าบริการ, เก็บสถานะ Session ผ่าน Thread Lock, เชื่อมต่อ SlipOK API และส่งคำสั่งพิมพ์
- **`views/index.html`**: หน้าเว็บแอปพลิเคชันแบบ Single Page ควบคุมการสลับหน้าย่อย (หน้าอัปโหลด, หน้าชำระเงิน, หน้าคิว และหน้าแจ้งเตือนข้อผิดพลาด) พร้อมทั้งจัดการ PDF Preview

---

### 🚀 การติดตั้งและเริ่มต้นใช้งาน (Getting Started)

ขั้นตอนการติดตั้งและทดสอบโปรเจกต์บนเครื่องของคุณ:

#### 1. โคลนคลังโค้ด (Clone Repository)
```bash
git clone https://github.com/Map2004/qprint-station.git
cd qprint-station
```

#### 2. สร้างและเปิดใช้งาน Virtual Environment
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Windows**:
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

#### 3. ติดตั้ง Dependencies
ติดตั้งแพ็กเกจที่จำเป็นด้วยคำสั่ง `pip`:
```bash
pip install bottle pypdf requests cheroot
```
*(หากมีไฟล์ `requirements.txt` สามารถใช้คำสั่ง):*
```bash
pip install -r requirements.txt
```

#### 4. รันเซิร์ฟเวอร์
```bash
python3 test.py
```
เปิดเว็บบราวเซอร์แล้วเข้าไปที่:  
👉 **`http://localhost:8080`**

---

### 💡 ขั้นตอนการใช้งาน (Usage)
1. **อัปโหลดเอกสาร**: เลือกไฟล์นามสกุล `.pdf` โดยระบบจะแสดงตัวอย่างหน้าแรกและจำนวนหน้าทั้งหมด
2. **เลือกตั้งค่าการพิมพ์**: กรอกหน้าที่ต้องการพิมพ์ (เช่น `1-3, 5`) หรือเว้นว่างเพื่อพิมพ์ทั้งหมด และเลือกโหมดสี/ขาวดำ จากนั้นกด **Upload**
3. **สแกนชำระเงิน**: ตรวจสอบยอดเงิน และใช้แอปพลิเคชันธนาคารสแกน QR Code พร้อมเพย์ที่ปรากฏ
4. **ส่งสลิปหลักฐาน**: แนบรูปภาพสลิปการโอนเงิน (`.png`, `.jpg`, `.jpeg`) แล้วกด **Upload**
5. **รับคิวการพิมพ์**: เมื่อระบบตรวจสอบสลิปผ่านแล้ว จะแสดงหมายเลขคิวการพิมพ์ของคุณทันที
