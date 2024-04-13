from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


class User(AbstractUser):
    pass

GRADE_CHOICES = [
    ("First_Class", "First Class"),
    ("Second_Class_Upper", "Second Class Upper"),
    ("Second_Class_Lower", "Second Class Lower"),
    ("Third_Class", "Third Class"),
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
    ("Med_Surg", "Medicine And Surgery"),
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
    
    # def save(self, *args, **kwargs):
    #     if not self.cert_code:
    #         while True:
    #             cert_code = str(uuid.uuid4().int)[:8]  # Generate a random 8-digit code
    #             if not StudentDetails.objects.filter(cert_code=cert_code).exists():
    #                 self.cert_code = cert_code
    #                 break
    #     super().save(*args, **kwargs)

class Certificate(models.Model):
    student = models.ForeignKey(StudentDetails, on_delete = models.CASCADE)
    pdf = models.FileField(upload_to="certificates/")