# Generated by Django 4.1.3 on 2022-11-05 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("body_craft_app", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="zenotiemployeesdata",
            old_name="Center",
            new_name="center",
        ),
    ]
