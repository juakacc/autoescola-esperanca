from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages as msgs
from django.shortcuts import render
from django.urls import reverse_lazy

from core.views.generics import ListView, CreateView, DeleteView, DetailView, UpdateView
from news.models import New
from news.forms import RegisterNewForm

from rolepermissions.mixins import HasPermissionsMixin

class IndexView(HasPermissionsMixin, ListView):
    required_permission = 'secretary'
    paginate_by = 10
    template_name = 'news/list_news_edit.html'
    model = New

class RegisterNewView(HasPermissionsMixin, SuccessMessageMixin, CreateView):
    required_permission = 'secretary'
    model = New
    template_name = 'news/register_new.html'
    form_class = RegisterNewForm
    success_url = reverse_lazy('news:list_news_edit')
    success_message = 'Notícia adicionada com sucesso'

class DeleteNewView(HasPermissionsMixin, DeleteView):
    required_permission = 'secretary'
    model = New
    success_url = reverse_lazy('news:list_news_edit')

    def delete(self, request, *args, **kwargs):
        msgs.success(request, 'Notícia removida com sucesso')
        return super().delete(request, *args, **kwargs)

class UpdateNewView(HasPermissionsMixin, SuccessMessageMixin, UpdateView):
    required_permission = 'secretary'
    model = New
    template_name = 'news/update_new.html'
    fields = ['title', 'slug', 'text', 'image']
    success_url = reverse_lazy('news:list_news_edit')
    success_message = 'Notícia atualizada com sucesso'

class DetailNewView(DetailView):
    model = New
    context_object_name = 'new'

index = IndexView.as_view()
register_new = RegisterNewView.as_view()
delete_new = DeleteNewView.as_view()
edit_new = UpdateNewView.as_view()
detail_new = DetailNewView.as_view()
