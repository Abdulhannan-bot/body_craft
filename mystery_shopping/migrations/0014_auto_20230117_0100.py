# Generated by Django 3.2.13 on 2023-01-16 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('body_craft_app', '0038_employeescheduler_remark'),
        ('mystery_shopping', '0013_mysteryshoppingoverview_service_agent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mysteryshoppingoverview',
            old_name='service_availed',
            new_name='paid_in_cash',
        ),
        migrations.RenameField(
            model_name='mysteryshoppingoverview',
            old_name='service_agent',
            new_name='service_agent_1',
        ),
        migrations.AddField(
            model_name='mysteryshoppingoverview',
            name='admin_reviewed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='mysteryshoppingoverview',
            name='auditor_completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='mysteryshoppingoverview',
            name='service_agent_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_agent_2', to='body_craft_app.extendedzenotiemployeesdata'),
        ),
        migrations.AddField(
            model_name='mysteryshoppingoverview',
            name='service_agent_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_agent_3', to='body_craft_app.extendedzenotiemployeesdata'),
        ),
        migrations.AddField(
            model_name='mysteryshoppingoverview',
            name='service_availed_1',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='mysteryshoppingoverview',
            name='service_availed_2',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='mysteryshoppingoverview',
            name='service_availed_3',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
