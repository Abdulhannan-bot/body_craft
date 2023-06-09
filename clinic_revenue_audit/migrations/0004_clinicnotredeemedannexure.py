# Generated by Django 3.2.13 on 2023-02-01 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic_revenue_audit', '0003_auto_20230201_0122'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClinicNotRedeemedAnnexure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_as_per_record', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=200, null=True)),
                ('client_name', models.CharField(blank=True, max_length=200, null=True)),
                ('category_of_sample', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity_of_not_redeemed', models.CharField(blank=True, max_length=200, null=True)),
                ('evidence', models.FileField(blank=True, null=True, upload_to='')),
                ('revenue_audit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic_revenue_audit.clinicrevenueauditoverview')),
            ],
        ),
    ]
