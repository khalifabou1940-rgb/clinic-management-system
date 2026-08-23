# -*- coding: utf-8 -*-
"""
خدمة التذكيرات والإشعارات
Reminder Service
"""

from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from src.database.db_manager import DatabaseManager
from src.database.models import Appointment
import threading

class ReminderService:
    """خدمة إدارة التذكيرات والإشعارات"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.scheduler = BackgroundScheduler()
        self.reminders_sent = []
    
    def start_scheduler(self):
        """بدء جدول التذكيرات"""
        try:
            # جدولة فحص التذكيرات كل ساعة
            self.scheduler.add_job(
                self.check_and_send_reminders,
                'interval',
                hours=1,
                id='appointment_reminder_job'
            )
            
            if not self.scheduler.running:
                self.scheduler.start()
            print("تم بدء خدمة التذكيرات بنجاح")
        except Exception as e:
            print(f"خطأ في بدء جدول التذكيرات: {e}")
    
    def stop_scheduler(self):
        """إيقاف جدول التذكيرات"""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
            print("تم إيقاف خدمة التذكيرات")
        except Exception as e:
            print(f"خطأ في إيقاف جدول التذكيرات: {e}")
    
    def check_and_send_reminders(self):
        """فحص وإرسال التذكيرات"""
        db = self.db_manager.get_session()
        try:
            # البحث عن المواعيد التي تحتاج تذكيرات
            tomorrow = (datetime.now() + timedelta(days=1)).date()
            
            appointments = db.query(Appointment).filter(
                Appointment.reminder_sent == False,
                Appointment.status == 'pending'
            ).all()
            
            for appointment in appointments:
                appointment_date = appointment.appointment_date.date() if isinstance(appointment.appointment_date, datetime) else appointment.appointment_date
                
                if appointment_date == tomorrow:
                    # إرسال التذكير
                    self.send_reminder(appointment)
                    
                    # تحديث حالة التذكير
                    appointment.reminder_sent = True
                    db.commit()
                    
                    # إضافة إلى السجل
                    self.reminders_sent.append({
                        'appointment_id': appointment.id,
                        'patient_name': appointment.patient.name_ar,
                        'appointment_date': str(appointment.appointment_date),
                        'sent_at': datetime.now()
                    })
        except Exception as e:
            print(f"خطأ في فحص التذكيرات: {e}")
        finally:
            db.close()
    
    def send_reminder(self, appointment):
        """إرسال تذكير للموعد"""
        try:
            patient = appointment.patient
            
            # إنشاء رسالة التذكير
            reminder_message_ar = f"""
            تذكير موعد طبي
            ================
            المريض: {patient.name_ar}
            الموعد: {appointment.appointment_date.strftime('%d/%m/%Y')} الساعة {appointment.appointment_time}
            السبب: {appointment.reason or 'فحص عام'}
            """
            
            reminder_message_fr = f"""
            Rappel de Rendez-vous
            ====================
            Patient: {patient.name_fr}
            Date: {appointment.appointment_date.strftime('%d/%m/%Y')} à {appointment.appointment_time}
            Motif: {appointment.reason or 'Consultation générale'}
            """
            
            # هنا يمكن إضافة طرق إرسال مختلفة (SMS, Email, إلخ)
            print(f"تم إرسال تذكير للمريض: {patient.name_ar}")
            print(reminder_message_ar)
            print(reminder_message_fr)
            
            return True
        except Exception as e:
            print(f"خطأ في إرسال التذكير: {e}")
            return False
    
    def send_manual_reminder(self, appointment_id):
        """إرسال تذكير يدوي"""
        db = self.db_manager.get_session()
        try:
            appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
            if appointment:
                self.send_reminder(appointment)
                return True
            return False
        finally:
            db.close()
    
    def get_reminders_history(self):
        """الحصول على سجل التذكيرات"""
        return self.reminders_sent
    
    def clear_reminders_history(self):
        """مسح سجل التذكيرات"""
        self.reminders_sent = []
    
    def resend_unsent_reminders(self):
        """إعادة إرسال التذكيرات غير المرسلة"""
        db = self.db_manager.get_session()
        try:
            unsent = db.query(Appointment).filter(
                Appointment.reminder_sent == False,
                Appointment.status == 'pending'
            ).all()
            
            for appointment in unsent:
                self.send_reminder(appointment)
                appointment.reminder_sent = True
                db.commit()
            
            return len(unsent)
        except Exception as e:
            print(f"خطأ في إعادة إرسال التذكيرات: {e}")
            return 0
        finally:
            db.close()
