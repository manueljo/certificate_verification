from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import qrcode
import uuid
from io import BytesIO
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# Create your models here.


class User(AbstractUser):
    pass

GRADE_CHOICES = [
    ("First Class", "First Class"),
    ("Second Class Upper", "Second Class Upper"),
    ("Second Class Lower", "Second Class Lower"),
    ("Third Class", "Third Class"),
]

FACULTY = [
    ("Science", "Science"),
    ("Engineering", "Engineering"),
    ("Law", "Law"),
    ("Medicals", "Medicals"),
]

DEPARTMENT = [
    ("Computer Science", "Computer Science"),
    ("Mechanical Engineering", "Mechanical Engineering"),
    ("Law", "Law"),
    ("Medicine And Surgery", "Medicine And Surgery"),
]

class StudentDetails(models.Model):
    cert_code = models.CharField(max_length=15, unique=True)
    surname = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    reg_number = models.CharField(max_length=20)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)
    faculty = models.CharField(max_length=20,choices=FACULTY)
    department = models.CharField(max_length=50, choices=DEPARTMENT)
    year_graduated = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Student Details'
        verbose_name_plural = 'Student Details'

    def __str__(self):
        return str(self.first_name)

    def save(self, *args, **kwargs):
        # self.generate_certificate()
        surname = self.surname
        firstname = self.first_name
        middle_name = self.middle_name
        dept = self.department

        while True:
            cert_code = str(uuid.uuid4().int)[:8]
            if not StudentDetails.objects.filter(cert_code=cert_code).exists():
                self.cert_code = cert_code
                break

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"Name: {surname}, Course: {dept}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert QR code to JPEG
        img_buffer = BytesIO()
        img.save(img_buffer, format='JPEG')
        img_buffer.seek(0)

        # Load university logo
        logo_path = BASE_DIR / 'static/images/crescent_logo.png'
        img_logo = Image.open(logo_path)

        # Generate PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        # Certificate number
        p.setFont("Helvetica", 10)
        p.drawString(450, 780, f"Certificate No: {self.cert_code}")

        # University logo
        img_logo_width, img_logo_height = img_logo.size
        logo_width = 200  # Adjust the width as needed
        logo_height = (logo_width / img_logo_width) * img_logo_height
        p.drawImage(logo_path, (letter[0] - logo_width) / 2, 550, width=logo_width, height=logo_height, mask='auto')

        # Certificate writeup
        p.setFont("Helvetica-Bold", 38)
        p.drawCentredString(letter[0] / 2, 500, f"Certificate of Achievement")
        p.setFont("Helvetica", 20)
        p.drawCentredString(letter[0] / 2, 450, f"This is to certify that")
        p.setFont("Helvetica", 25)
        p.drawCentredString(letter[0] / 2, 420, f"{surname} {firstname} {middle_name}")
        p.setFont("Helvetica", 15)
        p.drawCentredString(letter[0] / 2, 390, f"has successfully completed the course")
        p.setFont("Helvetica-Bold", 20)
        p.drawCentredString(letter[0] / 2, 360, f"{dept}")
        
        # Convert BytesIO to PIL Image
        pil_img = Image.open(img_buffer)

        p.drawInlineImage(pil_img, 250, 100,width=100, height=100)

        p.showPage()
        p.save()
        
        buffer.seek(0)

        super(StudentDetails, self).save(*args, **kwargs)
        cert = Certificate.objects.create(student=self)

        # Save PDF to database
        cert.pdf.save(f'certificate_{surname}.pdf', ContentFile(buffer.getvalue()))
        cert.save()




class Certificate(models.Model):
    student = models.ForeignKey(StudentDetails, on_delete = models.CASCADE)
    pdf = models.FileField(upload_to="certificates/")

    def __str__(self):
        return str(self.student.first_name)
    
    class Meta:
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'


    
class Bulk_Certificate(models.Model):
    excel_file = models.FileField(upload_to='excel_files/',)

    def __str__(self):
        return self.excel_file.name

    class Meta:
        verbose_name = 'Bulk Certificate'
        verbose_name_plural = 'Bulk Certificates'
    