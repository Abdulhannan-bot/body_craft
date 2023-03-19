# Generated by Django 3.2.13 on 2023-01-31 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon_revenue_audit', '0021_salonauditrepeatedquestion_checklist_series_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salonrevenueauditoverview',
            name='audit_period',
        ),
        migrations.AddField(
            model_name='salonrevenueauditoverview',
            name='audit_period_from',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='salonrevenueauditoverview',
            name='audit_period_to',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]