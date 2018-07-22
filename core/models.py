from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
    class Meta:
        verbose_name = 'Usuário'

class Vehicle(models.Model):
    STATE_CHOICES = (
        ('funcionando', 'Funcionando'),
        ('em conserto', 'Em conserto')
    )
    TYPE_CHOICES = (
        ('car', 'Carro'),
        ('motorcycle', 'Moto')
    )
    type = models.CharField('Tipo', max_length=20, choices=TYPE_CHOICES, default='motorcycle')
    fabricator = models.CharField('Fabricante', max_length=20)
    model = models.CharField('Modelo', max_length=20)
    year = models.PositiveIntegerField('Ano')
    plate = models.CharField('Placa', max_length=8, unique=True)
    state = models.CharField('Estado', max_length=20, choices=STATE_CHOICES, default='funcionando')

    def __str__(self):
        return "{}: [{}]".format(self.model, self.plate)

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

    def __str__(self):
        return 'Configurações do sistema'
