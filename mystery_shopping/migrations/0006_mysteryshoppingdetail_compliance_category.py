# Generated by Django 4.1.3 on 2022-12-20 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mystery_shopping", "0005_mysteryshoppingdetail_compliance_dropdown"),
    ]

    operations = [
        migrations.AddField(
            model_name="mysteryshoppingdetail",
            name="compliance_category",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
