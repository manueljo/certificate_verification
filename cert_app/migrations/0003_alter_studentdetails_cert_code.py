# Generated by Django 5.0.3 on 2024-05-30 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cert_app', '0002_bulk_certificate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdetails',
            name='cert_code',
            field=models.CharField(editable=False, max_length=15, unique=True),
        ),
    ]
