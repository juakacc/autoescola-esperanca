from django.db import models
from django.shortcuts import reverse

from accounts.models import Person

class Thread(models.Model):
    title = models.CharField('Título', max_length=100)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    body = models.TextField('Mensagem')
    author = models.ForeignKey(
        Person, verbose_name='Autor', related_name='threads', on_delete=models.CASCADE
    )
    views = models.IntegerField('Visualizações', blank=True, default=0)
    answers = models.IntegerField('Respostas', blank=True, default=0)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    modified_at = models.DateTimeField('Modificado em', auto_now=True)

    def get_absolute_url(self):
        return reverse('forum:thread', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-modified_at']

class Reply(models.Model):
    thread = models.ForeignKey(
        Thread, verbose_name='Tópico', related_name='replies', on_delete=models.CASCADE
    )
    reply = models.TextField('Resposta')
    author = models.ForeignKey(
        Person, verbose_name='Autor', related_name='replies', on_delete=models.CASCADE
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    modified_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-modified_at']

def update_count_replies(instance, **kwargs):
    ''' Atualiza o número de respostas a cada adição/exclusão '''
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()

models.signals.post_save.connect(
    update_count_replies, sender=Reply, dispatch_uid='update_count_replies'
)

models.signals.post_delete.connect(
    update_count_replies, sender=Reply, dispatch_uid='update_count_replies2'
)
