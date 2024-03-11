from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import qrcode
from io import BytesIO

from .forms import StudentDetailsForm
from .models import Certificate, StudentDetails

@login_required()
def generate_certificate(request):
    if request.method == 'POST':
        form = StudentDetailsForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['surname']
            dept = form.cleaned_data['department']
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f"Name: {name}, Course: {dept}")
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert QR code to JPEG
            img_buffer = BytesIO()
            img.save(img_buffer, format='JPEG')
            img_buffer.seek(0)

            # Generate PDF
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)

            # Customize PDF content
            p.setFont("Helvetica", 16)
            p.setFillColorRGB(0, 0, 0)  # Black color

            # Title
            p.drawCentredString(300, 750, "Certificate of Completion")

            # Student details
            p.setFont("Helvetica", 12)
            p.drawString(100, 700, f"Name: {name}")
            p.drawString(100, 680, f"Course: {dept}")
            
            # Convert BytesIO to PIL Image
            pil_img = Image.open(img_buffer)

            # Draw QR code on PDF
            #img.save(buffer, 'PNG')
            #buffer.seek(0)
            #p.drawInlineImage(buffer, 100, 600, width=100, height=100)
            p.drawInlineImage(pil_img, 100, 100,width=100, height=100)

            p.showPage()
            p.save()
            
            student = form.save()
            cert = Certificate(student=student)

            # Save PDF to database
            cert.pdf.save(f'certificate_{name}.pdf', ContentFile(buffer.getvalue()))
            cert.save()

            buffer.seek(0)
            
            # Return the PDF as a response
            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{name}_certificate.pdf"'
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