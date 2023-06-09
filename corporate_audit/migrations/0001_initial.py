# Generated by Django 4.1.3 on 2023-02-05 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("body_craft_app", "0041_alter_userprofile_user_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="CorporateAuditOverview",
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
                    "shopper_name",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("mobile", models.CharField(blank=True, max_length=200, null=True)),
                ("email", models.CharField(blank=True, max_length=200, null=True)),
                ("gender", models.CharField(blank=True, max_length=200, null=True)),
                ("start_time", models.TimeField(blank=True, max_length=200, null=True)),
                ("end_time", models.TimeField(blank=True, max_length=200, null=True)),
                ("date", models.DateField(blank=True, null=True)),
                (
                    "cost_of_service",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "invoice_number",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "paid_in_cash",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "payment_mode",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "amount_redeemed",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "contact_number_reached_for_appointment",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "auditor_completed",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "admin_reviewed",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                ("added_on", models.DateTimeField(auto_now_add=True)),
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
            name="CorporateAuditDetail",
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
                ("sequence", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "compliance_dropdown",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("date", models.DateField(blank=True, null=True)),
                (
                    "client_journey",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("kra", models.CharField(blank=True, max_length=200, null=True)),
                ("process", models.CharField(blank=True, max_length=200, null=True)),
                ("checklist", models.CharField(blank=True, max_length=1000, null=True)),
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
                    "relative_gaps_found",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                ("remark", models.CharField(blank=True, max_length=1000, null=True)),
                (
                    "service_number",
                    models.CharField(blank=True, max_length=200, null=True),
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
                    "center",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="body_craft_app.extendedzenoticenterdata",
                    ),
                ),
                (
                    "corporate_audit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="corporate_audit.corporateauditoverview",
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="body_craft_app.extendedzenotiemployeesdata",
                    ),
                ),
            ],
        ),
    ]
