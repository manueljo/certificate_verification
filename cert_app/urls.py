from django.urls import path
from . import views

urlpatterns = [
    path('', views.verify,name='verify'),
    path('generate/', views.generate_certificate,name='certificate'),
]
