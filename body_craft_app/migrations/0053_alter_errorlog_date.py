# Generated by Django 4.1.3 on 2023-03-16 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("body_craft_app", "0052_errorlog_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="errorlog",
            name="date",
            field=models.DateField(auto_now_add=True),
        ),
    ]