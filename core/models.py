from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from .constantes import *

class User(AbstractUser):
    pass
    class Meta:
        verbose_name = 'Usuário'
        unique_together = ('email',)

class Vehicle(models.Model):
    STATE_CHOICES = (
        (FUNCIONANDO, FUNCIONANDO),
        (EM_CONSERTO, EM_CONSERTO)
    )
    TYPE_CHOICES = (
        ('car', 'Carro'),
        ('motorcycle', 'Moto')
    )
    type = models.CharField('Tipo', max_length=20, choices=TYPE_CHOICES, default='motorcycle')
    slug = models.SlugField('Apelido', unique=True)
    fabricator = models.CharField('Fabricante', max_length=20)
    model = models.CharField('Modelo', max_length=20)
    year = models.PositiveIntegerField('Ano', default=datetime.now().year)
    plate = models.CharField('Placa', max_length=8, unique=True)
    state = models.CharField('Estado', max_length=20, choices=STATE_CHOICES, default=FUNCIONANDO)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['pk']

# Para contato de visitante com o administrador
class Contact(models.Model):
    name = models.CharField('Nome', max_length=100)
    email = models.EmailField('E-mail')
    subject = models.CharField('Assunto', max_length=100)
    message = models.TextField('Mensagem')
    visualized = models.BooleanField('Vista', default=False)
    response = models.TextField('Resposta', null=True)
    created = models.DateTimeField('Data', auto_now_add=True)

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
        ordering = ['-created']

class SystemSettings(models.Model):
    basic_salary = models.DecimalField('Salário Mínimo', max_digits=8, decimal_places=2)

    hours_theoretical = models.PositiveIntegerField('Horas teóricas')
    hours_practical_simulator = models.PositiveIntegerField('Horas práticas no simulador')
    hours_practical_vehicle = models.PositiveIntegerField('Horas práticas no veículo')

    # Para controle do agendamento
    begin_expedient = models.TimeField('Início do expediente', default='07:00', choices=HORARY)
    end_expedient = models.TimeField('Fim do expediente', default='18:00', choices=HORARY)

    def __str__(self):
        return 'Configurações do sistema'
