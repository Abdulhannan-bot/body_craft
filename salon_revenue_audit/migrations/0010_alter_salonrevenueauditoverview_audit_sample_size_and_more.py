# Generated by Django 4.1.3 on 2023-01-21 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "salon_revenue_audit",
            "0009_salonrevenueauditoverview_open_bill_audit_row_one_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="audit_sample_size",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="balance_in_happy_card",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="cash_in_hand",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="closing_balance_as_per_zenoti",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="custom_verification_as_per_counter",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="custom_verification_as_per_zenoti",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="custom_verification_reconciliation",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="no_of_appointment_as_per_zenoti_row_one",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="no_of_appointment_as_per_zenoti_row_two",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="no_of_blockout_notes_active",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="no_of_blockout_notes_deleted",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="no_of_clients_on_floor_row_one",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="no_of_clients_on_floor_row_two",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="no_of_issues_as_per_zenoti_for_rectification_bill",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="no_of_open_bill_row_one",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="no_of_open_bill_row_two",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="no_of_otp_overrides_as_per_zenoti",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="no_of_rectification_bill_as_per_zenoti",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="no_of_voucher_updated_on_zenoti",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="ob_as_per_pv",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="ob_as_per_statement",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="om_approved_otp_overrides",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="physcial_card_as_per_counter",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="physcial_card_as_per_zenoti",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="physcial_card_reconciliation",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="physical_cash_as_per_counter",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="physical_cash_as_per_zenoti",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="physical_cash_reconciliation",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="physical_voucher_available",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="remarks_with_voucher_number",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="total_no_of_audit_sample",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="total_no_of_membership_redeemed_for_campaign",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="salonrevenueauditoverview",
            name="total_no_of_nearby_transaction_in_zenoti",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
