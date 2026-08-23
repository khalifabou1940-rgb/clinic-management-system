# -*- coding: utf-8 -*-
"""
ملف الإعدادات العام للتطبيق
Application Configuration
"""

import os

# إعدادات قاعدة البيانات
DATABASE_PATH = 'data/clinic.db'
BACKUP_DIR = 'data/backups'
PRINTS_DIR = 'data/prints'

# إعدادات التطبيق
APP_NAME = 'نظام إدارة العيادة الطبية'
APP_VERSION = '1.0.0'
APP_AUTHOR = 'khalifabou1940-rgb'

# إعدادات المظهر
THEME_COLOR = '#003366'
BACKGROUND_COLOR = '#f5f5f5'
BUTTON_COLOR = '#003366'
BUTTON_HOVER_COLOR = '#004d99'

# إعدادات التذكيرات
REMINDER_HOURS_BEFORE = 24  # تذكير قبل 24 ساعة
REMINDER_CHECK_INTERVAL = 1  # فحص التذكيرات كل ساعة

# اللغات المدعومة
SUPPORTED_LANGUAGES = [
    ('ar', 'العربية'),
    ('fr', 'Français'),
]

DEFAULT_LANGUAGE = 'ar'

# إعدادات الطباعة
PRINT_CLINIC_NAME_AR = 'عيادتي الطبية'
PRINT_CLINIC_NAME_FR = 'Ma Clinique Médicale'
