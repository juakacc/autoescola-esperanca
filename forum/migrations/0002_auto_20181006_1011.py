# Generated by Django 2.0.7 on 2018-10-06 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reply',
            options={'ordering': ['-modified_at'], 'verbose_name': 'Resposta', 'verbose_name_plural': 'Respostas'},
        ),
    ]
