# -*- coding: utf-8 -*-
"""
صفحات واجهة المستخدم
UI Pages
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QDialog, QLabel, 
                             QLineEdit, QTextEdit, QDateTimeEdit, QComboBox, 
                             QFormLayout, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt, QDateTime, QDate
from PyQt5.QtGui import QFont, QColor
from src.services.patient_service import PatientService
from src.services.appointment_service import AppointmentService
from src.services.prescription_service import PrescriptionService
from src.services.visit_service import VisitService
from datetime import datetime

class DashboardPage(QWidget):
    """صفحة لوحة التحكم"""
    
    def __init__(self):
        super().__init__()
        self.patient_service = PatientService()
        self.appointment_service = AppointmentService()
        self.init_ui()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        layout = QVBoxLayout()
        
        title = QLabel("📊 لوحة التحكم | Tableau de Bord")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # إحصائيات
        stats_layout = QHBoxLayout()
        
        # عدد المرضى
        patients_count = self.patient_service.get_patient_count()
        patients_label = QLabel(f"👥 المرضى\nPatients\n{patients_count}")
        patients_label.setAlignment(Qt.AlignCenter)
        patients_label.setStyleSheet("background-color: #E3F2FD; padding: 20px; border-radius: 8px;")
        stats_layout.addWidget(patients_label)
        
        # مواعيد اليوم
        today_appointments = len(self.appointment_service.get_today_appointments())
        appointments_label = QLabel(f"📅 مواعيد اليوم\nRendez-vous d'aujourd'hui\n{today_appointments}")
        appointments_label.setAlignment(Qt.AlignCenter)
        appointments_label.setStyleSheet("background-color: #FFF3E0; padding: 20px; border-radius: 8px;")
        stats_layout.addWidget(appointments_label)
        
        layout.addLayout(stats_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def refresh(self):
        """تحديث البيانات"""
        self.init_ui()


class PatientsPage(QWidget):
    """صفحة إدارة المرضى"""
    
    def __init__(self):
        super().__init__()
        self.patient_service = PatientService()
        self.init_ui()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        layout = QVBoxLayout()
        
        # الأزرار العلوية
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ إضافة مريض جديد")
        add_btn.clicked.connect(self.add_patient)
        buttons_layout.addWidget(add_btn)
        
        delete_btn = QPushButton("❌ حذف المريض")
        delete_btn.clicked.connect(self.delete_patient)
        buttons_layout.addWidget(delete_btn)
        
        refresh_btn = QPushButton("🔄 تحديث")
        refresh_btn.clicked.connect(self.refresh)
        buttons_layout.addWidget(refresh_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # جدول المرضى
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["الرقم", "الاسم بالعربية", "الاسم بالفرنسية", "الهاتف", "البريد الإلكتروني", "التاريخ"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        self.load_patients()
    
    def load_patients(self):
        """تحميل المرضى"""
        patients = self.patient_service.get_all_patients()
        self.table.setRowCount(len(patients))
        
        for row, patient in enumerate(patients):
            self.table.setItem(row, 0, QTableWidgetItem(str(patient.id)))
            self.table.setItem(row, 1, QTableWidgetItem(patient.name_ar))
            self.table.setItem(row, 2, QTableWidgetItem(patient.name_fr or ""))
            self.table.setItem(row, 3, QTableWidgetItem(patient.phone))
            self.table.setItem(row, 4, QTableWidgetItem(patient.email or ""))
            self.table.setItem(row, 5, QTableWidgetItem(patient.created_at.strftime("%d/%m/%Y")))
    
    def add_patient(self):
        """إضافة مريض جديد"""
        dialog = AddPatientDialog()
        if dialog.exec_():
            self.patient_service.add_patient(**dialog.get_data())
            self.load_patients()
            QMessageBox.information(self, "نجاح", "تم إضافة المريض بنجاح")
    
    def delete_patient(self):
        """حذف المريض المحدد"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            patient_id = int(self.table.item(current_row, 0).text())
            reply = QMessageBox.question(self, "تأكيد", "هل تريد حذف هذا المريض؟")
            if reply == QMessageBox.Yes:
                self.patient_service.delete_patient(patient_id)
                self.load_patients()
                QMessageBox.information(self, "نجاح", "تم حذف المريض بنجاح")
    
    def refresh(self):
        """تحديث البيانات"""
        self.load_patients()


class AppointmentsPage(QWidget):
    """صفحة إدارة المواعيد"""
    
    def __init__(self):
        super().__init__()
        self.appointment_service = AppointmentService()
        self.patient_service = PatientService()
        self.init_ui()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        layout = QVBoxLayout()
        
        # الأزرار العلوية
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ حجز موعد جديد")
        add_btn.clicked.connect(self.add_appointment)
        buttons_layout.addWidget(add_btn)
        
        confirm_btn = QPushButton("✓ تأكيد الموعد")
        confirm_btn.clicked.connect(self.confirm_appointment)
        buttons_layout.addWidget(confirm_btn)
        
        complete_btn = QPushButton("✓✓ إنهاء الموعد")
        complete_btn.clicked.connect(self.complete_appointment)
        buttons_layout.addWidget(complete_btn)
        
        cancel_btn = QPushButton("❌ إلغاء الموعد")
        cancel_btn.clicked.connect(self.cancel_appointment)
        buttons_layout.addWidget(cancel_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # جدول المواعيد
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["الرقم", "المريض", "التاريخ", "الساعة", "السبب", "الحالة", "الملاحظات"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        self.load_appointments()
    
    def load_appointments(self):
        """تحميل المواعيد"""
        appointments = self.appointment_service.get_all_appointments()
        self.table.setRowCount(len(appointments))
        
        for row, appointment in enumerate(appointments):
            self.table.setItem(row, 0, QTableWidgetItem(str(appointment.id)))
            self.table.setItem(row, 1, QTableWidgetItem(appointment.patient.name_ar))
            self.table.setItem(row, 2, QTableWidgetItem(appointment.appointment_date.strftime("%d/%m/%Y")))
            self.table.setItem(row, 3, QTableWidgetItem(appointment.appointment_time))
            self.table.setItem(row, 4, QTableWidgetItem(appointment.reason or ""))
            status_item = QTableWidgetItem(appointment.status)
            if appointment.status == 'completed':
                status_item.setBackground(QColor('#4CAF50'))
            elif appointment.status == 'cancelled':
                status_item.setBackground(QColor('#F44336'))
            self.table.setItem(row, 5, status_item)
            self.table.setItem(row, 6, QTableWidgetItem(appointment.notes or ""))
    
    def add_appointment(self):
        """إضافة موعد جديد"""
        dialog = AddAppointmentDialog(self.patient_service)
        if dialog.exec_():
            self.appointment_service.add_appointment(**dialog.get_data())
            self.load_appointments()
            QMessageBox.information(self, "نجاح", "تم إضافة الموعد بنجاح")
    
    def confirm_appointment(self):
        """تأكيد الموعد"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            appointment_id = int(self.table.item(current_row, 0).text())
            self.appointment_service.confirm_appointment(appointment_id)
            self.load_appointments()
            QMessageBox.information(self, "نجاح", "تم تأكيد الموعد")
    
    def complete_appointment(self):
        """إنهاء الموعد"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            appointment_id = int(self.table.item(current_row, 0).text())
            self.appointment_service.complete_appointment(appointment_id)
            self.load_appointments()
            QMessageBox.information(self, "نجاح", "تم إنهاء الموعد")
    
    def cancel_appointment(self):
        """إلغاء الموعد"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            appointment_id = int(self.table.item(current_row, 0).text())
            reply = QMessageBox.question(self, "تأكيد", "هل تريد إلغاء هذا الموعد؟")
            if reply == QMessageBox.Yes:
                self.appointment_service.cancel_appointment(appointment_id)
                self.load_appointments()
                QMessageBox.information(self, "نجاح", "تم إلغاء الموعد")
    
    def refresh(self):
        """تحديث البيانات"""
        self.load_appointments()


class PrescriptionsPage(QWidget):
    """صفحة إدارة الوصفات الطبية"""
    
    def __init__(self):
        super().__init__()
        self.prescription_service = PrescriptionService()
        self.patient_service = PatientService()
        self.init_ui()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        layout = QVBoxLayout()
        
        # الأزرار العلوية
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ وصفة جديدة")
        add_btn.clicked.connect(self.add_prescription)
        buttons_layout.addWidget(add_btn)
        
        print_btn = QPushButton("🖨️ طباعة")
        print_btn.clicked.connect(self.print_prescription)
        buttons_layout.addWidget(print_btn)
        
        delete_btn = QPushButton("❌ حذف")
        delete_btn.clicked.connect(self.delete_prescription)
        buttons_layout.addWidget(delete_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # جدول الوصفات
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["الرقم", "المريض", "اسم الدواء", "الجرعة", "التكرار", "المدة", "تاريخ الإنشاء"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        self.load_prescriptions()
    
    def load_prescriptions(self):
        """تحميل الوصفات"""
        prescriptions = self.prescription_service.get_all_prescriptions()
        self.table.setRowCount(len(prescriptions))
        
        for row, prescription in enumerate(prescriptions):
            self.table.setItem(row, 0, QTableWidgetItem(str(prescription.id)))
            self.table.setItem(row, 1, QTableWidgetItem(prescription.patient.name_ar))
            self.table.setItem(row, 2, QTableWidgetItem(prescription.medication_name))
            self.table.setItem(row, 3, QTableWidgetItem(prescription.dosage or ""))
            self.table.setItem(row, 4, QTableWidgetItem(prescription.frequency or ""))
            self.table.setItem(row, 5, QTableWidgetItem(prescription.duration or ""))
            self.table.setItem(row, 6, QTableWidgetItem(prescription.created_at.strftime("%d/%m/%Y")))
    
    def add_prescription(self):
        """إضافة وصفة جديدة"""
        dialog = AddPrescriptionDialog(self.patient_service)
        if dialog.exec_():
            self.prescription_service.add_prescription(**dialog.get_data())
            self.load_prescriptions()
            QMessageBox.information(self, "نجاح", "تم إضافة الوصفة بنجاح")
    
    def print_prescription(self):
        """طباعة الوصفة"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            QMessageBox.information(self, "طباعة", "تم طباعة الوصفة بنجاح")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار وصفة للطباعة")
    
    def delete_prescription(self):
        """حذف الوصفة"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            prescription_id = int(self.table.item(current_row, 0).text())
            reply = QMessageBox.question(self, "تأكيد", "هل تريد حذف هذه الوصفة؟")
            if reply == QMessageBox.Yes:
                self.prescription_service.delete_prescription(prescription_id)
                self.load_prescriptions()
                QMessageBox.information(self, "نجاح", "تم حذف الوصفة بنجاح")
    
    def refresh(self):
        """تحديث البيانات"""
        self.load_prescriptions()


class VisitsPage(QWidget):
    """صفحة السجلات الطبية"""
    
    def __init__(self):
        super().__init__()
        self.visit_service = VisitService()
        self.patient_service = PatientService()
        self.init_ui()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        layout = QVBoxLayout()
        
        # الأزرار العلوية
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ زيارة جديدة")
        add_btn.clicked.connect(self.add_visit)
        buttons_layout.addWidget(add_btn)
        
        view_btn = QPushButton("👁️ عرض التفاصيل")
        view_btn.clicked.connect(self.view_visit)
        buttons_layout.addWidget(view_btn)
        
        delete_btn = QPushButton("❌ حذف")
        delete_btn.clicked.connect(self.delete_visit)
        buttons_layout.addWidget(delete_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # جدول الزيارات
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["الرقم", "المريض", "التاريخ", "الأعراض", "التشخيص", "العلاج"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        self.load_visits()
    
    def load_visits(self):
        """تحميل الزيارات"""
        visits = self.visit_service.get_all_visits()
        self.table.setRowCount(len(visits))
        
        for row, visit in enumerate(visits):
            self.table.setItem(row, 0, QTableWidgetItem(str(visit.id)))
            self.table.setItem(row, 1, QTableWidgetItem(visit.patient.name_ar))
            self.table.setItem(row, 2, QTableWidgetItem(visit.visit_date.strftime("%d/%m/%Y")))
            self.table.setItem(row, 3, QTableWidgetItem(visit.symptoms[:50] if visit.symptoms else ""))
            self.table.setItem(row, 4, QTableWidgetItem(visit.diagnosis[:50] if visit.diagnosis else ""))
            self.table.setItem(row, 5, QTableWidgetItem(visit.treatment[:50] if visit.treatment else ""))
    
    def add_visit(self):
        """إضافة زيارة جديدة"""
        dialog = AddVisitDialog(self.patient_service)
        if dialog.exec_():
            self.visit_service.add_visit(**dialog.get_data())
            self.load_visits()
            QMessageBox.information(self, "نجاح", "تم إضافة الزيارة بنجاح")
    
    def view_visit(self):
        """عرض تفاصيل الزيارة"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            visit_id = int(self.table.item(current_row, 0).text())
            QMessageBox.information(self, "التفاصيل", "تفاصيل الزيارة")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار زيارة")
    
    def delete_visit(self):
        """حذف الزيارة"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            visit_id = int(self.table.item(current_row, 0).text())
            reply = QMessageBox.question(self, "تأكيد", "هل تريد حذف هذه الزيارة؟")
            if reply == QMessageBox.Yes:
                self.visit_service.delete_visit(visit_id)
                self.load_visits()
                QMessageBox.information(self, "نجاح", "تم حذف الزيارة بنجاح")
    
    def refresh(self):
        """تحديث البيانات"""
        self.load_visits()


class SettingsPage(QWidget):
    """صفحة الإعدادات"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        layout = QVBoxLayout()
        
        title = QLabel("⚙️ الإعدادات | Paramètres")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # إعدادات النظام
        settings_label = QLabel("إعدادات النظام | Paramètres du Système")
        settings_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(settings_label)
        
        # إعدادات الشاشة
        language_label = QLabel("اللغة / Langue:")
        layout.addWidget(language_label)
        
        language_combo = QComboBox()
        language_combo.addItems(["العربية", "Français", "English"])
        layout.addWidget(language_combo)
        
        layout.addStretch()
        
        self.setLayout(layout)


# نوافذ الحوار
class AddPatientDialog(QDialog):
    """نافذة إضافة مريض جديد"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إضافة مريض جديد")
        self.setGeometry(100, 100, 400, 500)
        self.init_ui()
    
    def init_ui(self):
        """تهيئة الواجهة"""
        layout = QFormLayout()
        
        self.name_ar = QLineEdit()
        layout.addRow("الاسم بالعربية:", self.name_ar)
        
        self.name_fr = QLineEdit()
        layout.addRow("الاسم بالفرنسية:", self.name_fr)
        
        self.phone = QLineEdit()
        layout.addRow("رقم الهاتف:", self.phone)
        
        self.email = QLineEdit()
        layout.addRow("البريد الإلكتروني:", self.email)
        
        self.gender = QComboBox()
        self.gender.addItems(["ذكر", "أنثى"])
        layout.addRow("الجنس:", self.gender)
        
        self.address = QTextEdit()
        layout.addRow("العنوان:", self.address)
        
        self.medical_history = QTextEdit()
        layout.addRow("السجل الطبي:", self.medical_history)
        
        self.allergies = QTextEdit()
        layout.addRow("الحساسيات:", self.allergies)
        
        # أزرار
        button_layout = QHBoxLayout()
        
        ok_btn = QPushButton("حفظ")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addRow(button_layout)
        self.setLayout(layout)
    
    def get_data(self):
        """الحصول على البيانات المدخلة"""
        return {
            'name_ar': self.name_ar.text(),
            'name_fr': self.name_fr.text(),
            'phone': self.phone.text(),
            'email': self.email.text(),
            'date_of_birth': None,
            'gender': self.gender.currentText(),
            'address': self.address.toPlainText(),
            'medical_history': self.medical_history.toPlainText(),
            'allergies': self.allergies.toPlainText()
        }


class AddAppointmentDialog(QDialog):
    """نافذة إضافة موعد جديد"""
    
    def __init__(self, patient_service):
        super().__init__()
        self.patient_service = patient_service
        self.setWindowTitle("حجز موعد جديد")
        self.setGeometry(100, 100, 400, 400)
        self.init_ui()
    
    def init_ui(self):
        """تهيئة الواجهة"""
        layout = QFormLayout()
        
        self.patient = QComboBox()
        patients = self.patient_service.get_all_patients()
        for patient in patients:
            self.patient.addItem(patient.name_ar, patient.id)
        layout.addRow("المريض:", self.patient)
        
        self.appointment_date = QDateTimeEdit()
        self.appointment_date.setDateTime(QDateTime.currentDateTime())
        layout.addRow("التاريخ والوقت:", self.appointment_date)
        
        self.appointment_time = QLineEdit()
        layout.addRow("الساعة:", self.appointment_time)
        
        self.reason = QTextEdit()
        layout.addRow("السبب:", self.reason)
        
        self.notes = QTextEdit()
        layout.addRow("ملاحظات:", self.notes)
        
        # أزرار
        button_layout = QHBoxLayout()
        
        ok_btn = QPushButton("حفظ")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addRow(button_layout)
        self.setLayout(layout)
    
    def get_data(self):
        """الحصول على البيانات المدخلة"""
        return {
            'patient_id': self.patient.currentData(),
            'appointment_date': self.appointment_date.dateTime().toPyDateTime(),
            'appointment_time': self.appointment_time.text(),
            'reason': self.reason.toPlainText(),
            'notes': self.notes.toPlainText()
        }


class AddPrescriptionDialog(QDialog):
    """نافذة إضافة وصفة طبية"""
    
    def __init__(self, patient_service):
        super().__init__()
        self.patient_service = patient_service
        self.setWindowTitle("وصفة طبية جديدة")
        self.setGeometry(100, 100, 400, 500)
        self.init_ui()
    
    def init_ui(self):
        """تهيئة الواجهة"""
        layout = QFormLayout()
        
        self.patient = QComboBox()
        patients = self.patient_service.get_all_patients()
        for patient in patients:
            self.patient.addItem(patient.name_ar, patient.id)
        layout.addRow("المريض:", self.patient)
        
        self.medication_name = QLineEdit()
        layout.addRow("اسم الدواء:", self.medication_name)
        
        self.dosage = QLineEdit()
        layout.addRow("الجرعة:", self.dosage)
        
        self.frequency = QLineEdit()
        layout.addRow("التكرار:", self.frequency)
        
        self.duration = QLineEdit()
        layout.addRow("المدة:", self.duration)
        
        self.quantity = QLineEdit()
        layout.addRow("الكمية:", self.quantity)
        
        self.instructions = QTextEdit()
        layout.addRow("التعليمات:", self.instructions)
        
        # أزرار
        button_layout = QHBoxLayout()
        
        ok_btn = QPushButton("حفظ")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addRow(button_layout)
        self.setLayout(layout)
    
    def get_data(self):
        """الحصول على البيانات المدخلة"""
        return {
            'patient_id': self.patient.currentData(),
            'visit_id': None,
            'medication_name': self.medication_name.text(),
            'dosage': self.dosage.text(),
            'frequency': self.frequency.text(),
            'duration': self.duration.text(),
            'instructions': self.instructions.toPlainText(),
            'quantity': int(self.quantity.text()) if self.quantity.text() else 1
        }


class AddVisitDialog(QDialog):
    """نافذة إضافة زيارة طبية"""
    
    def __init__(self, patient_service):
        super().__init__()
        self.patient_service = patient_service
        self.setWindowTitle("زيارة طبية جديدة")
        self.setGeometry(100, 100, 400, 500)
        self.init_ui()
    
    def init_ui(self):
        """تهيئة الواجهة"""
        layout = QFormLayout()
        
        self.patient = QComboBox()
        patients = self.patient_service.get_all_patients()
        for patient in patients:
            self.patient.addItem(patient.name_ar, patient.id)
        layout.addRow("المريض:", self.patient)
        
        self.symptoms = QTextEdit()
        layout.addRow("الأعراض:", self.symptoms)
        
        self.diagnosis = QTextEdit()
        layout.addRow("التشخيص:", self.diagnosis)
        
        self.treatment = QTextEdit()
        layout.addRow("العلاج:", self.treatment)
        
        self.notes = QTextEdit()
        layout.addRow("ملاحظات:", self.notes)
        
        # أزرار
        button_layout = QHBoxLayout()
        
        ok_btn = QPushButton("حفظ")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addRow(button_layout)
        self.setLayout(layout)
    
    def get_data(self):
        """الحصول على البيانات المدخلة"""
        return {
            'patient_id': self.patient.currentData(),
            'symptoms': self.symptoms.toPlainText(),
            'diagnosis': self.diagnosis.toPlainText(),
            'treatment': self.treatment.toPlainText(),
            'notes': self.notes.toPlainText()
        }
