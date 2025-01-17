# Generated by Django 5.0.6 on 2024-10-28 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('midas', '0018_alter_scanner_strategy'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanner',
            name='time_frame',
            field=models.CharField(choices=[('Hour', 'Hour'), ('Day', 'Day'), ('Minute', 'Minute')], default='off'),
        ),
        migrations.AlterField(
            model_name='scanner',
            name='strategy',
            field=models.CharField(blank=True, choices=[('panda', 'Panda'), ('cat', 'Cat'), ('coyote', 'Coyote')], null=True),
        ),
        migrations.AlterField(
            model_name='symbol',
            name='indexes',
            field=models.ManyToManyField(blank=True, related_name='symbol_index', to='midas.index', verbose_name='indexes'),
        ),
        migrations.AlterField(
            model_name='symbol',
            name='industries',
            field=models.ManyToManyField(blank=True, related_name='industry_index', to='midas.industry', verbose_name='indexes'),
        ),
    ]
