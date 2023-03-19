# Generated by Django 4.1.3 on 2023-02-05 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("body_craft_app", "0040_alter_userprofile_user_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="user_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("staff", "staff"),
                    ("admin", "admin"),
                    ("Audit Admin", "Audit Admin"),
                    ("Mystery Shopper", "Mystery Shopper"),
                    ("Salon Revenue Auditor", "Salon Revenue Auditor"),
                    ("Clinic Revenue Auditor", "Clinic Revenue Auditor"),
                ],
                max_length=100,
            ),
        ),
    ]