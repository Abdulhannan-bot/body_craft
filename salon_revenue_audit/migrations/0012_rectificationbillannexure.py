# Generated by Django 3.2.13 on 2023-01-23 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salon_revenue_audit', '0011_deletedserviceannexure'),
    ]

    operations = [
        migrations.CreateModel(
            name='RectificationBillAnnexure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_no', models.CharField(blank=True, max_length=500, null=True)),
                ('issue_no', models.CharField(blank=True, max_length=500, null=True)),
                ('remark', models.CharField(blank=True, max_length=500, null=True)),
                ('revenue_audit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='salon_revenue_audit.salonrevenueauditoverview')),
            ],
        ),
    ]