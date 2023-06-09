# Generated by Django 4.1.3 on 2023-03-15 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("body_craft_app", "0047_extendedzenoticenterdata_center_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="ErrorLog",
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
                ("page", models.CharField(blank=True, max_length=200, null=True)),
                ("sentence", models.TextField(blank=True, null=True)),
                ("added_date", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "employee",
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
