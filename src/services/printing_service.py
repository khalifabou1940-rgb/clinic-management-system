# -*- coding: utf-8 -*-
"""
خدمة طباعة الوصفات الطبية
Prescription Printing Service
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from datetime import datetime
import os

class PrintingService:
    """خدمة طباعة الوصفات والتقارير"""
    
    def __init__(self):
        self.output_dir = 'data/prints'
        os.makedirs(self.output_dir, exist_ok=True)
        self.clinic_name_ar = "عيادتي الطبية"
        self.clinic_name_fr = "Ma Clinique Médicale"
    
    def print_prescription(self, prescription_data, patient_data, doctor_name):
        """طباعة وصفة طبية"""
        try:
            filename = f"prescription_{prescription_data['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            # إنشاء مستند PDF
            doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=1*cm, leftMargin=1*cm,
                                   topMargin=1*cm, bottomMargin=1*cm)
            
            # عناصر المستند
            elements = []
            styles = getSampleStyleSheet()
            
            # عنوان العيادة
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#003366'),
                spaceAfter=6,
                alignment=1  # center
            )
            
            elements.append(Paragraph(self.clinic_name_ar, title_style))
            elements.append(Paragraph(self.clinic_name_fr, title_style))
            elements.append(Spacer(1, 0.3*cm))
            
            # معلومات الوصفة
            data = [
                ['المريض / Patient:', f"{patient_data.get('name_ar', '')} / {patient_data.get('name_fr', '')}"],
                ['رقم الملف / Dossier:', str(patient_data.get('id', ''))],
                ['التاريخ / Date:', datetime.now().strftime('%d/%m/%Y')],
            ]
            
            table = Table(data, colWidths=[2.5*cm, 12*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F0F7')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 0.5*cm))
            
            # معلومات الدواء
            elements.append(Paragraph("<b>التعليمات الطبية / Instructions Médicales:</b>", styles['Heading2']))
            elements.append(Spacer(1, 0.2*cm))
            
            med_data = [
                ['اسم الدواء / Médicament:', prescription_data.get('medication_name', '')],
                ['الجرعة / Dosage:', prescription_data.get('dosage', '')],
                ['التكرار / Fréquence:', prescription_data.get('frequency', '')],
                ['المدة / Durée:', prescription_data.get('duration', '')],
                ['الكمية / Quantité:', str(prescription_data.get('quantity', ''))],
                ['عدد مرات التكرار / Renouvellements:', str(prescription_data.get('refills', 0))],
            ]
            
            med_table = Table(med_data, colWidths=[4*cm, 10*cm])
            med_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FFE6E6')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            
            elements.append(med_table)
            elements.append(Spacer(1, 0.5*cm))
            
            # ملاحظات إضافية
            if prescription_data.get('instructions'):
                elements.append(Paragraph("<b>ملاحظات / Notes:</b>", styles['Heading3']))
                elements.append(Paragraph(prescription_data.get('instructions', ''), styles['Normal']))
                elements.append(Spacer(1, 0.5*cm))
            
            # توقيع الطبيب
            elements.append(Spacer(1, 0.8*cm))
            elements.append(Paragraph(f"<b>الطبيب / Médecin: {doctor_name}</b>", styles['Normal']))
            elements.append(Paragraph(f"التاريخ: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
            
            # بناء المستند
            doc.build(elements)
            return filepath
        except Exception as e:
            print(f"خطأ في طباعة الوصفة: {e}")
            return None
    
    def print_medical_report(self, patient_data, visit_data, filename_prefix='report'):
        """طباعة تقرير طبي"""
        try:
            filename = f"{filename_prefix}_{patient_data.get('id', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=1*cm, leftMargin=1*cm,
                                   topMargin=1*cm, bottomMargin=1*cm)
            
            elements = []
            styles = getSampleStyleSheet()
            
            # عنوان التقرير
            title_style = ParagraphStyle(
                'ReportTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#003366'),
                spaceAfter=6,
                alignment=1
            )
            
            elements.append(Paragraph(self.clinic_name_ar, title_style))
            elements.append(Paragraph("التقرير الطبي / Rapport Médical", title_style))
            elements.append(Spacer(1, 0.3*cm))
            
            # معلومات المريض
            patient_info = [
                ['الاسم / Nom:', f"{patient_data.get('name_ar', '')} / {patient_data.get('name_fr', '')}"],
                ['الهاتف / Téléphone:', patient_data.get('phone', '')],
                ['تاريخ الميلاد / Date de Naissance:', str(patient_data.get('date_of_birth', ''))],
                ['الجنس / Sexe:', patient_data.get('gender', '')],
            ]
            
            info_table = Table(patient_info, colWidths=[3*cm, 11*cm])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F0F7')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            
            elements.append(info_table)
            elements.append(Spacer(1, 0.4*cm))
            
            # معلومات الزيارة
            elements.append(Paragraph("<b>تفاصيل الزيارة / Détails de la Visite:</b>", styles['Heading2']))
            elements.append(Spacer(1, 0.2*cm))
            
            visit_info = [
                ['الأعراض / Symptômes:', visit_data.get('symptoms', '')],
                ['التشخيص / Diagnostic:', visit_data.get('diagnosis', '')],
                ['العلاج / Traitement:', visit_data.get('treatment', '')],
            ]
            
            visit_table = Table(visit_info, colWidths=[3*cm, 11*cm])
            visit_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FFE6E6')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            
            elements.append(visit_table)
            elements.append(Spacer(1, 0.5*cm))
            
            # ملاحظات
            if visit_data.get('notes'):
                elements.append(Paragraph("<b>ملاحظات إضافية / Remarques:</b>", styles['Heading3']))
                elements.append(Paragraph(visit_data.get('notes', ''), styles['Normal']))
            
            elements.append(Spacer(1, 0.8*cm))
            elements.append(Paragraph(f"تم إصدار التقرير في: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
            
            doc.build(elements)
            return filepath
        except Exception as e:
            print(f"خطأ في طباعة التقرير: {e}")
            return None
