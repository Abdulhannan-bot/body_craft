# Generated by Django 3.2.13 on 2023-03-06 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('body_craft_app', '0043_auto_20230306_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_category',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_type_name',
            field=models.ManyToManyField(to='body_craft_app.UserType'),
        ),
    ]
