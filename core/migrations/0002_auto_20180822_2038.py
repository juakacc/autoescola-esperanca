# Generated by Django 2.0.7 on 2018-08-22 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('email',)},
        ),
    ]
