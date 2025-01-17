# Generated by Django 5.0.6 on 2024-05-19 12:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("midas", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="indicatorcondition",
            name="code",
            field=models.CharField(default="None", max_length=50, verbose_name="Code"),
        ),
        migrations.AddField(
            model_name="scanner",
            name="name",
            field=models.CharField(default="None", max_length=50, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="indicator",
            name="code",
            field=models.CharField(default="None", max_length=50, verbose_name="Code"),
        ),
    ]
