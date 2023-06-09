# Generated by Django 4.1.3 on 2022-11-06 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("body_craft_app", "0006_remove_zenotiemployeesdata_center_code_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ASSOCIATED_ROLE_OPTIONS",
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
                ("option", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="WEEK_OFF_OPTIONS",
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
                ("option", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ExtendedZenotiEmployeesData",
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
                    "office_start_time",
                    models.TimeField(blank=True, max_length=100, null=True),
                ),
                (
                    "office_end_time",
                    models.TimeField(blank=True, max_length=100, null=True),
                ),
                (
                    "associated_center",
                    models.ManyToManyField(
                        blank=True, to="body_craft_app.zenoticentersdata"
                    ),
                ),
                (
                    "associated_role",
                    models.ManyToManyField(
                        blank=True, to="body_craft_app.associated_role_options"
                    ),
                ),
                (
                    "week_off",
                    models.ManyToManyField(
                        blank=True, to="body_craft_app.week_off_options"
                    ),
                ),
                (
                    "zenoti_data",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="body_craft_app.zenotiemployeesdata",
                    ),
                ),
            ],
        ),
    ]
