# Generated by Django 3.2.13 on 2023-01-19 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon_revenue_audit', '0005_alter_hygieneannexure_sample_dates'),
    ]

    operations = [
        migrations.AddField(
            model_name='salonrevenueauditoverview',
            name='no_of_clients_on_floor',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='salonrevenueauditoverview',
            name='no_of_open_bill',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
