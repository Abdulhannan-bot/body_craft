# Generated by Django 4.1.3 on 2022-12-22 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("body_craft_app", "0036_delete_mysteryshoppingoverview"),
        ("mystery_shopping", "0009_auto_20221222_0012"),
    ]

    operations = [
        migrations.CreateModel(
            name="MysteryShoppingImages",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(blank=True, null=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, default="profile1.jpg", null=True, upload_to=""
                    ),
                ),
                (
                    "center",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="body_craft_app.extendedzenoticenterdata",
                    ),
                ),
                (
                    "mystery_shopping",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mystery_shopping.mysteryshoppingoverview",
                    ),
                ),
            ],
        ),
    ]