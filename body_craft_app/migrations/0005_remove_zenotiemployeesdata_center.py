# Generated by Django 4.1.3 on 2022-11-06 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("body_craft_app", "0004_alter_zenotiemployeesdata_center"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="zenotiemployeesdata",
            name="center",
        ),
    ]
