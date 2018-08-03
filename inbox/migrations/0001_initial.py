# Generated by Django 2.0.7 on 2018-07-30 00:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='Assunto')),
                ('message', models.TextField(verbose_name='Mensagem')),
                ('visualized', models.BooleanField(default=False, verbose_name='Vista')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('response', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='inbox.Message')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enviados', to='accounts.Person', verbose_name='Remetente')),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recebidos', to='accounts.Person', verbose_name='Destinatário')),
            ],
            options={
                'verbose_name_plural': 'Mensagens',
                'ordering': ['-created'],
                'verbose_name': 'Mensagem',
            },
        ),
    ]