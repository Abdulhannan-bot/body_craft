# Generated by Django 4.1.3 on 2023-02-06 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("corporate_audit", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="corporateauditdetail",
            name="client_journey",
        ),
        migrations.RemoveField(
            model_name="corporateauditdetail",
            name="process",
        ),
    ]
