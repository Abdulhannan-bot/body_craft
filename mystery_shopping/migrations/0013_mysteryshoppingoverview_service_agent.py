# Generated by Django 4.1.3 on 2022-12-28 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("body_craft_app", "0036_delete_mysteryshoppingoverview"),
        ("mystery_shopping", "0012_remove_mysteryshoppingoverview_amount_in_cash"),
    ]

    operations = [
        migrations.AddField(
            model_name="mysteryshoppingoverview",
            name="service_agent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="body_craft_app.extendedzenotiemployeesdata",
            ),
        ),
    ]
