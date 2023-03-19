# Generated by Django 4.1.3 on 2022-11-18 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("body_craft_app", "0020_alter_employeescheduler_center"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employeescheduler",
            name="center",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="body_craft_app.zenoticentersdata",
            ),
        ),
        migrations.AlterField(
            model_name="employeescheduler",
            name="employee",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="body_craft_app.extendedzenotiemployeesdata",
            ),
        ),
    ]
