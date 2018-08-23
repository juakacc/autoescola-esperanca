from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import RegisterMessageForm, RegisterResponseForm
from .models import Message
from accounts.models import Person
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages as messages_django
from django.core.exceptions import PermissionDenied

from core.views.generics import ListView, CreateView, DetailView, DeleteView
from watson import search as watson
from rolepermissions.mixins import HasPermissionsMixin

class ListMessagesReceivedView(HasPermissionsMixin, ListView):
    required_permission = 'student'
    template_name = 'inbox/list_messages_received.html'
    context_object_name = 'msgs'
    paginate_by = 10

    def get_queryset(self):
        query =  Message.objects.filter(to__pk=self.request.user.pk, not_view=False)
        q = self.request.GET.get('q', '')
        if q:
            query = watson.filter(query, q)
        return query

class ListMessagesSentView(HasPermissionsMixin, ListView):
    required_permission = 'student'
    template_name = 'inbox/list_messages_sent.html'
    context_object_name = 'msgs'
    paginate_by = 10

    def get_queryset(self):
        query = Message.objects.filter(sender__pk=self.request.user.pk)
        q = self.request.GET.get('q', '')
        if q:
            query = watson.filter(query, q)
        return query

class ListMessagesHidden(HasPermissionsMixin, ListView):
    required_permission = 'student'
    template_name = 'inbox/list_messages_received.html'
    context_object_name = 'msgs'
    paginate_by = 10

    def get_queryset(self):
        query = Message.objects.filter(to__pk=self.request.user.pk, not_view=True)
        q = self.request.GET.get('q', '')
        if q:
            query = watson.filter(query, q)
        return query

class DetailMessageView(HasPermissionsMixin, CreateView):
    ''' View para detalhar uma mensagem enviada/recebida, no último caso
    é possível registrar uma resposta '''
    required_permission = 'student'
    template_name = 'inbox/detail_message.html'
    model = Message
    form_class = RegisterResponseForm

    def get_initial(self):
        message = Message.objects.get(pk=self.kwargs['message_pk'])

        return {
            'message_text' : message.response
        }

    def form_valid(self, form):
        response = form.save(commit=False)
        message = self.get_context_data().get('message')
        response.to = message.sender
        response.sender = message.to
        response.subject = 'RES: {}'.format(message.subject)
        response.save()
        message.response = response
        message.save()
        messages_django.success(self.request, 'Resposta enviada com sucesso')
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        message = Message.objects.get(pk=self.kwargs['message_pk'])
        sender = message.sender.pk
        to = message.to.pk
        user = self.request.user.pk

        if sender != user and to != user: # Só exibir template se o usuário for o sender ou o to da mensagem
            raise PermissionDenied

        if message.sender.pk == self.request.user.pk:
            context['is_mine'] = True
        else:
            context['is_mine'] = False
            message.visualized = True
            message.save()
        context['message'] = message
        return context

class RegisterMessageView(HasPermissionsMixin, SuccessMessageMixin, CreateView):
    required_permission = 'student'
    form_class = RegisterMessageForm
    model = Message
    template_name = 'inbox/register_message.html'
    success_message = 'Mensagem enviada com sucesso'

    def get_initial(self):
        to = self.kwargs.get('person_pk', '')
        if to:
            to = Person.objects.get(pk=to)

        return {
            'to': to,
            'subject': self.kwargs.get('subject', 'Sem assunto')
        }

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.sender = Person.objects.get(pk=self.request.user.pk)
        self.object.save()
        return super().form_valid(form)

class DeleteMessageView(DeleteView):
    ''' View para ocultar uma determinada mensagem '''
    model = Message
    success_url = reverse_lazy('inbox:list_messages_received')

    def delete(self, request, *args, **kwargs):
        mensagem = self.get_object()
        mensagem.not_view = True
        mensagem.save()
        messages_django.success(self.request, 'Mensagem oculta com sucesso')
        return HttpResponseRedirect(self.get_success_url())

list_messages_received = ListMessagesReceivedView.as_view()
list_messages_sent = ListMessagesSentView.as_view()
list_messages_hidden = ListMessagesHidden.as_view()

register_message = RegisterMessageView.as_view()
detail_message = DetailMessageView.as_view()
delete_message = DeleteMessageView.as_view()
