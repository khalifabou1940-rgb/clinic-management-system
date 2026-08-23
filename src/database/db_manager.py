# -*- coding: utf-8 -*-
"""
إدارة قاعدة البيانات
Database Manager
"""

import os
import shutil
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.database.models import Base, User, Patient, Appointment, Visit, Prescription, Backup
import hashlib

class DatabaseManager:
    """مدير قاعدة البيانات"""
    
    def __init__(self):
        self.db_path = 'data/clinic.db'
        self.backup_dir = 'data/backups'
        self.engine = None
        self.SessionLocal = None
        self._create_directories()
    
    def _create_directories(self):
        """إنشاء المجلدات المطلوبة"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def initialize_database(self):
        """تهيئة قاعدة البيانات"""
        db_url = f'sqlite:///{self.db_path}'
        self.engine = create_engine(db_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # إنشاء الجداول
        Base.metadata.create_all(bind=self.engine)
        
        # إنشاء مستخدم افتراضي
        self._create_default_user()
    
    def _create_default_user(self):
        """إنشاء مستخدم افتراضي"""
        db = self.SessionLocal()
        try:
            # التحقق من وجود مستخدمين
            user_count = db.query(User).count()
            if user_count == 0:
                # إنشاء طبيب افتراضي
                password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
                default_doctor = User(
                    username='doctor',
                    password=password_hash,
                    full_name_ar='الدكتور',
                    full_name_fr='Le Docteur',
                    email='doctor@clinic.local',
                    role='doctor',
                    is_active=True
                )
                db.add(default_doctor)
                
                # إنشاء مساعد افتراضي
                default_assistant = User(
                    username='assistant',
                    password=password_hash,
                    full_name_ar='المساعد',
                    full_name_fr='L\'Assistant',
                    email='assistant@clinic.local',
                    role='assistant',
                    is_active=True
                )
                db.add(default_assistant)
                db.commit()
        except Exception as e:
            print(f"خطأ في إنشاء المستخدم الافتراضي: {e}")
        finally:
            db.close()
    
    def get_session(self) -> Session:
        """الحصول على جلسة قاعدة البيانات"""
        return self.SessionLocal()
    
    def create_backup(self) -> bool:
        """إنشاء نسخة احتياطية"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(self.backup_dir, f'clinic_backup_{timestamp}.db')
            
            # نسخ ملف قاعدة البيانات
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, backup_file)
            
            # حفظ معلومات النسخة الاحتياطية
            db = self.SessionLocal()
            try:
                backup_size = os.path.getsize(backup_file) / (1024 * 1024)  # تحويل إلى MB
                backup = Backup(
                    backup_path=backup_file,
                    backup_size=backup_size,
                    status='success'
                )
                db.add(backup)
                db.commit()
            finally:
                db.close()
            
            return True
        except Exception as e:
            print(f"خطأ في إنشاء النسخة الاحتياطية: {e}")
            return False
    
    def restore_backup(self, backup_path: str) -> bool:
        """استعادة نسخة احتياطية"""
        try:
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, self.db_path)
                return True
        except Exception as e:
            print(f"خطأ في استعادة النسخة الاحتياطية: {e}")
        return False
    
    def get_backups_list(self):
        """الحصول على قائمة النسخ الاحتياطية"""
        db = self.SessionLocal()
        try:
            backups = db.query(Backup).order_by(Backup.backup_date.desc()).all()
            return backups
        finally:
            db.close()
    
    def close(self):
        """إغلاق قاعدة البيانات"""
        if self.engine:
            self.engine.dispose()
