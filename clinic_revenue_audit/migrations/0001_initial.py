# Generated by Django 4.1.3 on 2023-01-29 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("body_craft_app", "0039_userprofile_user_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClinicRevenueAuditOverview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(blank=True, null=True)),
                (
                    "auditor_name",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "audit_period",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("added_on", models.DateTimeField(auto_now_add=True)),
                (
                    "total_discount_cases_as_per_zenoti",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "total_approvals_verified",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "dicount_cases_remark",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "total_membership_redemption_as_per_zenoti",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "membership_redemption_remark",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "rectification_tracker_maintained",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "no_of_rectification_bill_as_per_zenoti",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "no_of_issues_as_per_zenoti_rectification",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "added_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="body_craft_app.userprofile",
                    ),
                ),
                (
                    "center",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="body_craft_app.extendedzenoticenterdata",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ClinicRectificationBillAnnexure",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bill_no", models.CharField(blank=True, max_length=200, null=True)),
                ("issue_no", models.CharField(blank=True, max_length=200, null=True)),
                ("remark", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "revenue_audit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="clinic_revenue_audit.clinicrevenueauditoverview",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ClinicOtherObservationAnnexure",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "observation_area",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "audit_findings",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "revenue_audit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="clinic_revenue_audit.clinicrevenueauditoverview",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ClinicHygieneCheckAnnexure",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sample_dates",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "total_guest",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "sample_size_for_audit",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "invoice_date",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "invoice_number",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "client_name",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "category_of_sample",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "quantity_of_injectable_as_per_bill",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "quantity_of_injectable_as_per_consent_form",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "quantity_of_injectable_as_per_treatment_record",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "consumable_bill_quantity_matching_as_per_treatment_record",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "reception_copy",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "security_copy",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "security_sheet",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "feedback_updated",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "job_card_attached",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "job_card_matches_invoice",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "client_profile_form",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "disclaimer_form",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "consent_form",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "client_signature_matching_all_docs",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "treatment_record_entry",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "customer_signature_treatment_record",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "doctor_signature_treatment_record",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "redemption_of_all_service_under_right_package",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "consultant_signature",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("remark", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "revenue_audit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="clinic_revenue_audit.clinicrevenueauditoverview",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ClinicDeletedServiceAnnexure",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "designation",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "no_of_services_deleted",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "deleted_without_proper_justification",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("remark", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "revenue_audit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="clinic_revenue_audit.clinicrevenueauditoverview",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ClinicAuditRepeatedQuestion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("checklist", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "responsible_kra",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "relative_gap_found",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("compliance", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "compliance_category",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "compliance_category_percentage",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "action_taken_by_outlet_manager",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "status_by_om",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "remark_by_om",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                (
                    "action_taken_by_management",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "remark_by_management",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                (
                    "expected_dept_intervene",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "remark_by_department",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                (
                    "status_by_department",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "person_responsible",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="body_craft_app.extendedzenotiemployeesdata",
                    ),
                ),
                (
                    "revenue_audit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clinic_revenue_audit",
                        to="clinic_revenue_audit.clinicrevenueauditoverview",
                    ),
                ),
            ],
        ),
    ]
