# Generated by Django 3.2.13 on 2023-01-31 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon_revenue_audit', '0022_auto_20230131_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salonrevenueauditoverview',
            name='audit_period_from',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salonrevenueauditoverview',
            name='audit_period_to',
            field=models.DateField(blank=True, null=True),
        ),
    ]
