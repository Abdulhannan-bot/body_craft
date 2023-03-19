# Generated by Django 4.1.3 on 2023-01-15 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("salon_revenue_audit", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="custom_verification_as_per_counter",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="custom_verification_as_per_zenoti",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="custom_verification_reconciliation",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="physcial_card_as_per_counter",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="physcial_card_as_per_zenoti",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="physcial_card_reconciliation",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="physical_cash_as_per_counter",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="physical_cash_as_per_zenoti",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="physical_cash_reconciliation",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
