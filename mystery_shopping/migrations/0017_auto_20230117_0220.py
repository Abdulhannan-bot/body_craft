# Generated by Django 3.2.13 on 2023-01-16 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystery_shopping', '0016_remove_mysteryshoppingoverview_service_availed_1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mysteryshoppingdetail',
            name='service_availed',
        ),
        migrations.AddField(
            model_name='mysteryshoppingoverview',
            name='service_availed_1',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]