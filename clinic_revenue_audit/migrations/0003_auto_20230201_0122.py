# Generated by Django 3.2.13 on 2023-01-31 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic_revenue_audit', '0002_auto_20230131_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinicauditrepeatedquestion',
            name='question_series',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='clinicauditrepeatedquestion',
            name='tab_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]