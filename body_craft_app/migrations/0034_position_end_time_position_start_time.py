# Generated by Django 4.1.3 on 2022-12-09 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("body_craft_app", "0033_zenotiemployeesdata_employee_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="position",
            name="end_time",
            field=models.TimeField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="position",
            name="start_time",
            field=models.TimeField(blank=True, max_length=100, null=True),
        ),
    ]
