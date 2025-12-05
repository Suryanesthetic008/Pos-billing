
# 💻 Lakshmi Krishna Net Centre – Offline POS Billing System
A fully offline, lightweight, Kivy-based POS (Point of Sale) software designed for Indian Net Centres, Print Shops, Xerox Shops, and Small Businesses.

This software runs on **Windows PC (Python)** and **Android (via APK build)** without any internet connection.  
All data is stored in a secure local SQLite database.

---

## ✨ Features

### 🔹 Billing System
- Add multiple services to a bill  
- Automatic bill numbering (`LKNC-00001` format)  
- Quantity & discount support  
- Auto total calculation  
- Save customer name & payment method  
- Offline-only — no server needed  

### 🔹 Service Management
- Add / Edit / Delete services  
- Supports category, name, unit, and price  
- Auto-load into billing module  

### 🔹 Payment Method Management
- Add or remove payment methods  
- Works instantly with billing  

### 🔹 Credit Customer System (Udhaar)
- Add customers  
- Track due amount  
- Ledger with debit/credit entries  
- Auto-total due calculation  

### 🔹 Expenses Module
- Track daily expenses  
- Category, amount, notes  
- Expense history view  

### 🔹 Reports System
- Daily report  
- Monthly report  
- Custom date range  
- Service-wise summary  
- Payment-wise summary  
- Export to:
  - PDF  
  - Word (.docx)  
  - Excel (.csv)  

### 🔹 Dashboard (Analytics)
- Today's sales  
- Total bills today  
- Top service  
- Monthly sales graph (Matplotlib)  

### 🔹 Counters System
Track daily:
- Print pages  
- Xerox pages  
- Scan count  

### 🔹 Tools
- Offline backup  
- Offline restore  

### 🔹 Settings
- Shop name, owner name, address  
- Phone number  
- Upload custom logo  
- Choose theme (light, dark, blue)  

---

## 📁 Project Structure

LakshmiPOS/ │ ├── main.py ├── requirements.txt ├── README.md │ ├── database/ │     └── db.py │ ├── screens/ │     ├── billing.py │     ├── services.py │     ├── payments.py │     ├── customers.py │     ├── expenses.py │     ├── reports.py │     ├── counters.py │     ├── tools.py │     ├── settings.py │     └── dashboard.py │ └── ui/ ├── main.kv └── components.kv

---

## 🔧 Installation (Windows PC)

### Step 1 — Install Python
Download from: https://python.org

### Step 2 — Install dependencies

pip install -r requirements.txt

### Step 3 — Run the App

python main.py

---

## 🤖 Build Android APK

Install Buildozer (Linux only — requires WSL or Ubuntu VPS):

pip install buildozer buildozer -v android debug

APK will appear in:

bin/*.apk

---

## 💾 Database
The app uses:
- **SQLite (pos_data.db)**  
- Auto-backup created daily  

---

## 🖼 Logo Support
Upload logo via:
**Settings → Upload Logo**

Logo saved as:

assets/logo.png

---

## 🛡 Offline Mode
All features run **100% offline**.  
No cloud.  
No server.  
No internet required.  

---

## 👤 Author
**Surya Prakash** (Lakshmi Krishna Net Centre)  
Custom POS system created with ChatGPT assistance.

---

## 📜 License
This project is private and created for Lakshmi Krishna Net Centre.  
Not for resale unless permitted by the owner.


---
