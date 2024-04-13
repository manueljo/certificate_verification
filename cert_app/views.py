from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import qrcode
import uuid
from io import BytesIO
from pathlib import Path
from .forms import StudentDetailsForm
from .models import Certificate, StudentDetails


BASE_DIR = Path(__file__).resolve().parent.parent

@login_required()
def generate_certificate(request):
    if not request.user.is_staff:
        return redirect('verify')
    
    if request.method == 'POST':
        form = StudentDetailsForm(request.POST)
        if form.is_valid():
            # Get form data
            surname = form.cleaned_data['surname']
            firstname = form.cleaned_data['first_name']
            middle_name = form.cleaned_data['middle_name']
            dept = form.cleaned_data['department']

            while True:
                cert_code = str(uuid.uuid4().int)[:8]
                if not StudentDetails.objects.filter(cert_code=cert_code).exists():
                    break
            
            # Generate QR code
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
            p.drawString(450, 780, f"Certificate No: {cert_code}")

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
            
            instance = form.save(commit=False)
            instance.cert_code = cert_code 
            instance.save()
            cert = Certificate(student=instance)

            # Save PDF to database
            cert.pdf.save(f'certificate_{surname}.pdf', ContentFile(buffer.getvalue()))
            cert.save()

            buffer.seek(0)
            
            # Return the PDF as a response
            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{surname}_certificate.pdf"'
            return response
    else:
        form = StudentDetailsForm()

    return render(request, 'upload.html', {'form': form})


def verify(request):
    if request.method == 'POST':
        certificate = request.POST.get('code')
        
        if StudentDetails.objects.filter(cert_code=certificate).exists():
            details = StudentDetails.objects.get(cert_code=certificate)
            context = {'details':details}
            return render(request, 'index.html#verification',context)
        else:
            details = None
            context = {'details':details}
            return render(request, 'index.html#verification',context)
    
    context = {}
    return render(request, 'index.html',context)