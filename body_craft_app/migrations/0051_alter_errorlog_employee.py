# Generated by Django 4.1.3 on 2023-03-16 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("body_craft_app", "0050_alter_userprofile_roster_access"),
    ]

    operations = [
        migrations.AlterField(
            model_name="errorlog",
            name="employee",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="body_craft_app.userprofile",
            ),
        ),
    ]
