# Generated by Django 3.2.13 on 2023-02-15 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mystery_shopping', '0022_auto_20230214_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='mysteryshoppingdetail',
            name='month_of_audit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mystery_shopping.monthaudit'),
        ),
    ]
