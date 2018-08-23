# Generated by Django 2.0.7 on 2018-08-22 23:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=500, unique=True, verbose_name='Chave')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('confirmed', models.BooleanField(default=False, verbose_name='Confirmado?')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resets', to='accounts.Person', verbose_name='Usuário')),
            ],
            options={
                'verbose_name_plural': 'Novas Senhas',
                'verbose_name': 'Nova Senha',
            },
        ),
    ]
