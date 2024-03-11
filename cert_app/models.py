from django.db import models
from django.contrib.auth.models import AbstractUser

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
    ("Comp_Science", "Computer Science"),
    ("Mech_Engine", "Mechanical Engineering"),
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
    department = models.CharField(max_length=20, choices=DEPARTMENT)
    year_graduated = models.CharField(max_length=20)
    
class Certificate(models.Model):
    student = models.ForeignKey(StudentDetails, on_delete = models.CASCADE)
    pdf = models.FileField(upload_to="certificates/")