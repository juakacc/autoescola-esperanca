# Generated by Django 2.0.7 on 2018-12-02 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20180822_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='state',
            field=models.CharField(choices=[('Funcionando', 'Funcionando'), ('Em conserto', 'Em conserto')], default='Funcionando', max_length=20, verbose_name='Estado'),
        ),
    ]