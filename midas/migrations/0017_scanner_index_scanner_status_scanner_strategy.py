# Generated by Django 5.0.6 on 2024-10-22 14:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('midas', '0016_index_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanner',
            name='index',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='midas.index'),
        ),
        migrations.AddField(
            model_name='scanner',
            name='status',
            field=models.CharField(choices=[('on', 'on'), ('off', 'Off')], default='off'),
        ),
        migrations.AddField(
            model_name='scanner',
            name='strategy',
            field=models.CharField(blank=True, choices=('panda', 'Panda'), null=True),
        ),
    ]