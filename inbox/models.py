from django.db import models
from accounts.models import Person
from watson import search as watson

class Message(models.Model):

    sender = models.ForeignKey(Person, verbose_name='Remetente', related_name='enviados', on_delete=models.CASCADE)
    to = models.ForeignKey(Person, verbose_name='Destinatário', related_name='recebidos', on_delete=models.CASCADE)
    subject = models.CharField('Assunto', max_length=100, default='Sem assunto', blank=True)
    message_text = models.TextField('Mensagem')
    visualized = models.BooleanField('Vista', default=False)
    response = models.OneToOneField('self', null=True, on_delete=models.SET_NULL)

    created = models.DateTimeField('Data', auto_now_add=True)
    not_view = models.BooleanField('Ocultar', default=False)

    def __str__(self):
        return self.message_text

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        ordering = ['-created']

watson.register(Message)
