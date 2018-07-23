# Generated by Django 2.0.7 on 2018-07-22 00:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_systemsettings'),
        ('process', '0009_auto_20180720_2224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='practicalcourse',
            name='vehicle',
        ),
        migrations.AddField(
            model_name='practicalclass',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Vehicle', verbose_name='Veículo'),
        ),
        migrations.AlterField(
            model_name='practicalclass',
            name='day',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Dia da aula'),
        ),
        migrations.AlterField(
            model_name='practicalclass',
            name='end_time',
            field=models.TimeField(verbose_name='Hora do fim'),
        ),
        migrations.AlterField(
            model_name='practicalclass',
            name='simulator',
            field=models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=False, verbose_name='Aula de simulador'),
        ),
        migrations.AlterField(
            model_name='practicalclass',
            name='start_time',
            field=models.TimeField(verbose_name='Hora do início'),
        ),
    ]