# Generated by Django 3.2.13 on 2023-01-18 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon_revenue_audit', '0002_alter_salonrevenueauditoverview_custom_verification_as_per_counter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salonrevenueauditoverview',
            name='custom_verification_as_per_counter',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salonrevenueauditoverview',
            name='custom_verification_as_per_zenoti',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salonrevenueauditoverview',
            name='custom_verification_reconciliation',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salonrevenueauditoverview',
            name='physcial_card_as_per_counter',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salonrevenueauditoverview',
            name='physcial_card_as_per_zenoti',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salonrevenueauditoverview',
            name='physcial_card_reconciliation',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salonrevenueauditoverview',
            name='physical_cash_as_per_counter',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salonrevenueauditoverview',
            name='physical_cash_as_per_zenoti',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salonrevenueauditoverview',
            name='physical_cash_reconciliation',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]