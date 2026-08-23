# 📋 دليل التثبيت
# Installation Guide

## المتطلبات - Requirements

- **Python 3.8+** أو أحدث
- **pip** (مدير حزم Python)
- **Windows 10+** أو **macOS 10.14+** أو **Linux (Ubuntu 18.04+)**

---

## خطوات التثبيت على Windows 🪟

### 1. تثبيت Python
1. اذهب إلى https://www.python.org/downloads/
2. حمّل Python 3.10 أو أحدث
3. افتح المثبت وتأكد من تحديد "Add Python to PATH"
4. اضغط "Install Now"

### 2. التحقق من التثبيت
افتح Command Prompt واكتب:
```bash
python --version
```

يجب أن تظهر نسخة Python المثبتة.

### 3. استنساخ أو تحميل المشروع

**الخيار 1: استخدام Git**
```bash
git clone https://github.com/khalifabou1940-rgb/clinic-management-system.git
cd clinic-management-system
```

**الخيار 2: تحميل ZIP**
1. اذهب إلى: https://github.com/khalifabou1940-rgb/clinic-management-system
2. اضغط على "Code" ثم "Download ZIP"
3. فك ضغط الملف
4. افتح Command Prompt من المجلد

### 4. تثبيت المكتبات
في Command Prompt اكتب:
```bash
pip install -r requirements.txt
```

### 5. تشغيل البرنامج
```bash
python main.py
```

---

## خطوات التثبيت على macOS 🍎

### 1. تثبيت Python
استخدم Homebrew:
```bash
brew install python@3.10
```

### 2. التحقق من التثبيت
```bash
python3 --version
```

### 3. استنساخ المشروع
```bash
git clone https://github.com/khalifabou1940-rgb/clinic-management-system.git
cd clinic-management-system
```

### 4. إنشاء بيئة افتراضية (اختياري)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 6. تشغيل البرنامج
```bash
python3 main.py
```

---

## خطوات التثبيت على Linux 🐧

### 1. تثبيت Python والأدوات المطلوبة
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-dev git
```

### 2. استنساخ المشروع
```bash
git clone https://github.com/khalifabou1940-rgb/clinic-management-system.git
cd clinic-management-system
```

### 3. إنشاء بيئة افتراضية
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 5. إعطاء صلاحيات التنفيذ
```bash
chmod +x main.py
```

### 6. تشغيل البرنامج
```bash
python3 main.py
```

---

## استكشاف الأخطاء الشائعة 🔧

### الخطأ: "python: command not found"
**الحل:**
- تأكد من تثبيت Python بشكل صحيح
- جرب `python3` بدلاً من `python`
- في Windows، أعد تثبيت Python وحدد "Add Python to PATH"

### الخطأ: "No module named PyQt5"
**الحل:**
```bash
pip install PyQt5==5.15.7
```

### الخطأ: "pip: command not found"
**الحل:**
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### الخطأ: "Permission denied" على Linux
**الحل:**
```bash
sudo chmod +x main.py
sudo python3 main.py
```

---

## البيئة الافتراضية (مستحسن) 🏗️

من الأفضل استخدام بيئة افتراضية:

### الإنشاء
```bash
python -m venv venv
```

### التفعيل
**على Windows:**
```bash
venv\Scripts\activate
```

**على macOS/Linux:**
```bash
source venv/bin/activate
```

### تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### إلغاء التفعيل
```bash
deactivate
```

---

## التحديث 🔄

للحصول على أحدث النسخة:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## المساعدة والدعم 💬

إذا واجهت أي مشاكل:

1. تحقق من ملف README.md
2. ابحث عن issue موجودة على GitHub
3. أنشئ issue جديدة بوصف المشكلة

---

**تم! البرنامج جاهز للاستخدام** ✅
