# Generated by Django 3.2.13 on 2022-12-06 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('body_craft_app', '0032_alter_userprofile_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='zenotiemployeesdata',
            name='employee_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
