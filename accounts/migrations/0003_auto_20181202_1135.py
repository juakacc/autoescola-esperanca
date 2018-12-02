# Generated by Django 2.0.7 on 2018-12-02 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_passwordreset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='cpf',
            field=models.CharField(max_length=14, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='person',
            name='role_admin',
            field=models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=False, verbose_name='Admin?'),
        ),
        migrations.AlterField(
            model_name='person',
            name='role_instructor',
            field=models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=False, verbose_name='Instrutor?'),
        ),
        migrations.AlterField(
            model_name='person',
            name='role_secretary',
            field=models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=False, verbose_name='Secretário?'),
        ),
        migrations.AlterField(
            model_name='person',
            name='role_student',
            field=models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=False, verbose_name='Aluno?'),
        ),
    ]