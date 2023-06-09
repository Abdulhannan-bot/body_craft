# Generated by Django 3.2.13 on 2022-12-15 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('body_craft_app', '0034_position_end_time_position_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(blank=True, choices=[('staff', 'staff'), ('admin', 'admin'), ('Audit Admin', 'Audit Admin'), ('Mystery Shopper', 'Mystery Shopper')], max_length=100),
        ),
        migrations.CreateModel(
            name='MysteryShoppingOverview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopper_name', models.CharField(blank=True, max_length=200, null=True)),
                ('mobile', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('gender', models.CharField(blank=True, max_length=200, null=True)),
                ('start_time', models.TimeField(blank=True, max_length=200, null=True)),
                ('end_time', models.TimeField(blank=True, max_length=200, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('service_availed', models.CharField(blank=True, max_length=500, null=True)),
                ('cost_of_service', models.CharField(blank=True, max_length=200, null=True)),
                ('invoice_number', models.CharField(blank=True, max_length=200, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='body_craft_app.userprofile')),
                ('center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='body_craft_app.extendedzenoticenterdata')),
            ],
        ),
    ]
