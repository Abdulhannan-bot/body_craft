# Generated by Django 4.1.3 on 2022-11-20 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("body_craft_app", "0023_extendedzenotiemployeesdata_position"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="extendedzenotiemployeesdata",
            name="position",
        ),
        migrations.AddField(
            model_name="extendedzenoticenterdata",
            name="position",
            field=models.ManyToManyField(blank=True, to="body_craft_app.position"),
        ),
    ]
