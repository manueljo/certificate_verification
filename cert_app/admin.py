from django.contrib import admin
from django.core.files.base import ContentFile
from django.db import transaction
from .models import StudentDetails, Certificate, Bulk_Certificate
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import qrcode
import uuid
from io import BytesIO
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent


class BulkCertificateAdmin(admin.ModelAdmin):
    list_display = ('excel_file',)
    actions = ['generate_certificates']

    def generate_certificates(self, request, queryset):
        for bulk_cert in queryset:
            # Read the Excel file
            excel_file = bulk_cert.excel_file.read()
            df = pd.read_excel(BytesIO(excel_file))
            
            for index, row in df.iterrows():
                surname=row['Surname']
                first_name=row['First Name']
                middle_name=row['Middle Name']
                reg_number=row['Reg. Number']
                grade=row['Grade']
                faculty=row['Faculty']
                department=row['Department']
                year_graduated=row['Year Graduated']

                # Create or get the student details
                student = StudentDetails.objects.create(
                    surname=surname,
                    first_name=first_name,
                    middle_name=middle_name,
                    reg_number=reg_number,
                    grade=grade,
                    faculty=faculty,
                    department=department,
                    year_graduated=year_graduated
                )
                print(f'student code {student.cert_code}')

    
    generate_certificates.short_description = 'Generate Certificates'

admin.site.register(StudentDetails)
admin.site.register(Certificate)
admin.site.register(Bulk_Certificate, BulkCertificateAdmin)
