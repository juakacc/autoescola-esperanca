from django.db import models
from django.urls import reverse

class New(models.Model):
    title = models.CharField('Título', max_length=100)
    slug = models.SlugField('Identificador', max_length=200, unique=True)
    text = models.TextField('Notícia')
    image = models.ImageField('Imagem', upload_to='news', blank=True, null=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    modified_at = models.DateTimeField('Modificado em', auto_now=True)

    def get_absolute_url(self):
        return reverse('news:detail_new', kwargs={'slug': self.slug})

    def __str__(self):
        return self.slug
