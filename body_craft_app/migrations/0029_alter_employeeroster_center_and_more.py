# Generated by Django 4.1.3 on 2022-12-01 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("body_craft_app", "0028_extendedzenotiemployeesdata_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employeeroster",
            name="center",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="body_craft_app.extendedzenoticenterdata",
            ),
        ),
        migrations.AlterField(
            model_name="employeeroster",
            name="employee",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="body_craft_app.extendedzenotiemployeesdata",
            ),
        ),
        migrations.AlterField(
            model_name="employeescheduler",
            name="center",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="body_craft_app.extendedzenoticenterdata",
            ),
        ),
        migrations.AlterField(
            model_name="extendedzenotiemployeesleavedata",
            name="zenoti_data",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="body_craft_app.extendedzenotiemployeesdata",
            ),
        ),
    ]
