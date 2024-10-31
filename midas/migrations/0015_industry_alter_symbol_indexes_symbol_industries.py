# Generated by Django 5.0.6 on 2024-10-18 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('midas', '0014_symbol_indexes_alter_index_ticker'),
    ]

    operations = [
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1023, null=True, verbose_name='Name')),
            ],
        ),
        migrations.AlterField(
            model_name='symbol',
            name='indexes',
            field=models.ManyToManyField(related_name='symbol_index', to='midas.index', verbose_name=''),
        ),
        migrations.AddField(
            model_name='symbol',
            name='industries',
            field=models.ManyToManyField(related_name='industry_index', to='midas.industry', verbose_name=''),
        ),
    ]