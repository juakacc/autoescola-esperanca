from django.db import models

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
