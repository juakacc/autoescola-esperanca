from django.db import models
from django.urls import reverse
from datetime import datetime

from core.models import User
from core.constantes import *

class Person(User):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField('Nome', max_length=100)
    cpf = models.CharField('CPF', max_length=11, unique=True)
    date_of_birth = models.DateField('Data de nascimento')
    telephone = models.CharField('Telefone', max_length=20)
    street = models.CharField('Rua', max_length=200)
    number = models.PositiveIntegerField('Número')
    district = models.CharField('Bairro', max_length=100)
    city = models.CharField('Cidade', max_length=100)
    state = models.CharField('Estado', max_length=2,
        choices=STATES_CHOICE, default='PB')

    created = models.DateTimeField('Criado em', auto_now_add=True)

    role_admin = models.BooleanField('Admin?', default=False)
    role_secretary = models.BooleanField('Secretário?', default=False)
    role_instructor = models.BooleanField('Instrutor?', default=False)
    role_student = models.BooleanField('Aluno?', default=False)
    current_view = models.CharField('Visão atual', max_length=20, null=True, blank=True) # visão atual do site

    registry = models.CharField('Matrícula', max_length=10, null=True, blank=True) # Automaticamente
    salary = models.DecimalField(verbose_name='Salário', max_digits=8, decimal_places=2, default=950.00)
    admission = models.DateField('Admitido em', default=datetime.today, null=True, blank=True)
    # Instrutores
    cnh = models.CharField('CNH', max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_cpf_display(self):
        return '{}.{}.{}-{}'.format(self.cpf[:3], self.cpf[3:6], self.cpf[6:9], self.cpf[9:])

    def get_absolute_url(self):
        return reverse('accounts:detail_employee', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ['name']
