# Generated by Django 5.0.6 on 2024-06-09 14:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("midas", "0010_indicatorinstance_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="indicatorinstance",
            name="code",
            field=models.TextField(blank=True, null=True, verbose_name="Code"),
        ),
        migrations.AlterField(
            model_name="indicatorinstance",
            name="indicator",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="midas.indicator",
            ),
        ),
        migrations.AlterField(
            model_name="indicatorinstance",
            name="setup",
            field=models.JSONField(blank=True, null=True, verbose_name="setup"),
        ),
    ]