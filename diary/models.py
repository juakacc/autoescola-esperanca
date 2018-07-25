from django.db import models
from datetime import datetime
from accounts.models import Employee
from process.models import Process

class Appointment(models.Model):

    instructor = models.ForeignKey(Employee, verbose_name='Instrutor', on_delete=models.CASCADE)
    process = models.ForeignKey(Process, verbose_name='Processo', on_delete=models.CASCADE)
    simulator = models.BooleanField('Aula no simulador', default=False,
        choices=((True, 'Sim'), (False, 'Não'))
    )
    day = models.DateField('Dia', default=datetime.now)
    begin_time = models.TimeField('Início')
    end_time = models.TimeField('Fim')

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['day']
        unique_together = ('process', 'day', 'begin_time')
