# Generated by Django 3.2.13 on 2023-02-02 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic_revenue_audit', '0004_clinicnotredeemedannexure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicnotredeemedannexure',
            name='evidence',
            field=models.FileField(blank=True, null=True, upload_to='media'),
        ),
    ]
