# forms.py
from django import forms
from .models import *

class StudentDetailsForm(forms.ModelForm):
    class Meta:
        model = StudentDetails
        fields = '__all__'
        exclude = ('cert_code',)
