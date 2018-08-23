from datetime import datetime
from django.db import models
from django.urls import reverse
from accounts.models import Person
from process.models import Process
from core.models import HORARY

class Appointment(models.Model):

    instructor = models.ForeignKey(Person, verbose_name='Instrutor', on_delete=models.CASCADE)
    process = models.ForeignKey(Process, verbose_name='Processo', on_delete=models.CASCADE)
    simulator = models.BooleanField('Aula no simulador', default=False,
        choices=((True, 'Sim'), (False, 'Não'))
    )
    day = models.DateField('Dia', default=datetime.now)
    begin_time = models.TimeField('Início', choices=HORARY)
    end_time = models.TimeField('Fim', choices=HORARY)

    def get_absolute_url(self):
        return reverse('diary:detail_appointment', kwargs={'pk': self.pk})

    def __str__(self):
        return 'Agendamento do processo #{}'.format(self.process.pk)

    def get_slug(self):
        return 'Agendamento #{}'.format(self.pk)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['day']
        unique_together = ('process', 'day', 'begin_time')
