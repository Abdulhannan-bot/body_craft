# Generated by Django 4.1.3 on 2022-11-16 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("body_craft_app", "0015_extendedzenotiemployeesleavedata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="extendedzenoticenterdata",
            name="zenoti_data",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="body_craft_app.zenoticentersdata",
            ),
        ),
    ]
