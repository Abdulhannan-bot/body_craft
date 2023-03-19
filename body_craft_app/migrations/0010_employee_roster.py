# Generated by Django 3.2.13 on 2022-11-09 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('body_craft_app', '0009_alter_extendedzenotiemployeesdata_associated_role_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee_roster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appoint_date', models.DateField()),
                ('office_start_time', models.TimeField(blank=True, max_length=100, null=True)),
                ('office_end_time', models.TimeField(blank=True, max_length=100, null=True)),
                ('associated_role', models.ManyToManyField(blank=True, to='body_craft_app.AssociatedRoleOptions')),
                ('center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='body_craft_app.zenoticentersdata')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='body_craft_app.zenotiemployeesdata')),
            ],
        ),
    ]
