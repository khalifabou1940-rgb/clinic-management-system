# -*- coding: utf-8 -*-
"""
خدمة إدارة السجلات الطبية
Visit Service
"""

from src.database.db_manager import DatabaseManager
from src.database.models import Visit
from datetime import datetime

class VisitService:
    """خدمة إدارة السجلات الطبية للزيارات"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def add_visit(self, patient_id, symptoms, diagnosis, treatment, notes):
        """إضافة زيارة طبية جديدة"""
        db = self.db_manager.get_session()
        try:
            visit = Visit(
                patient_id=patient_id,
                symptoms=symptoms,
                diagnosis=diagnosis,
                treatment=treatment,
                notes=notes
            )
            db.add(visit)
            db.commit()
            return visit.id
        except Exception as e:
            db.rollback()
            print(f"خطأ في إضافة الزيارة: {e}")
            return None
        finally:
            db.close()
    
    def get_all_visits(self):
        """الحصول على جميع الزيارات"""
        db = self.db_manager.get_session()
        try:
            visits = db.query(Visit).order_by(Visit.visit_date.desc()).all()
            return visits
        finally:
            db.close()
    
    def get_patient_visits(self, patient_id):
        """الحصول على زيارات المريض"""
        db = self.db_manager.get_session()
        try:
            visits = db.query(Visit).filter(
                Visit.patient_id == patient_id
            ).order_by(Visit.visit_date.desc()).all()
            return visits
        finally:
            db.close()
    
    def get_visit(self, visit_id):
        """الحصول على زيارة محددة"""
        db = self.db_manager.get_session()
        try:
            visit = db.query(Visit).filter(Visit.id == visit_id).first()
            return visit
        finally:
            db.close()
    
    def update_visit(self, visit_id, **kwargs):
        """تحديث الزيارة"""
        db = self.db_manager.get_session()
        try:
            visit = db.query(Visit).filter(Visit.id == visit_id).first()
            if visit:
                for key, value in kwargs.items():
                    if hasattr(visit, key):
                        setattr(visit, key, value)
                visit.updated_at = datetime.now()
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"خطأ في تحديث الزيارة: {e}")
            return False
        finally:
            db.close()
    
    def delete_visit(self, visit_id):
        """حذف الزيارة"""
        db = self.db_manager.get_session()
        try:
            visit = db.query(Visit).filter(Visit.id == visit_id).first()
            if visit:
                db.delete(visit)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"خطأ في حذف الزيارة: {e}")
            return False
        finally:
            db.close()
