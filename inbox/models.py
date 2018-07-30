from django.db import models
from accounts.models import Person

class Message(models.Model):

    sender = models.ForeignKey(Person, verbose_name='Remetente', related_name='enviados', on_delete=models.CASCADE)
    to = models.ForeignKey(Person, verbose_name='Destinatário', related_name='recebidos', on_delete=models.CASCADE)
    subject = models.CharField('Assunto', max_length=100, default='Sem assunto', blank=True)
    message = models.TextField('Mensagem')
    visualized = models.BooleanField('Vista', default=False)
    response = models.ForeignKey('self', related_name='respostas', null=True, on_delete=models.CASCADE)

    created = models.DateTimeField('Data', auto_now_add=True)

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        ordering = ['-created']
