# Generated by Django 4.1.3 on 2022-12-17 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mystery_shopping", "0002_mysteryshoppingdetail"),
    ]

    operations = [
        migrations.RenameField(
            model_name="mysteryshoppingdetail",
            old_name="Compliance",
            new_name="compliance",
        ),
    ]
