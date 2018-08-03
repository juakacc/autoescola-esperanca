from .forms import RegisterMessageForm, RegisterResponseForm
from .models import Message
from accounts.models import Person
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied

from core.views.generics import ListView, CreateView, DetailView

from rolepermissions.mixins import HasPermissionsMixin

class ListMessagesReceivedView(HasPermissionsMixin, ListView):
    required_permission = 'student'
    template_name = 'inbox/list_messages_received.html'
    context_object_name = 'msgs'

    def get_queryset(self):
        return Message.objects.filter(to__pk=self.request.user.pk)

class ListMessagesSentView(HasPermissionsMixin, ListView):
    required_permission = 'student'
    template_name = 'inbox/list_messages_sent.html'
    context_object_name = 'msgs'

    def get_queryset(self):
        return Message.objects.filter(sender__pk=self.request.user.pk)

class DetailMessageView(HasPermissionsMixin, CreateView):
    required_permission = 'student'
    template_name = 'inbox/detail_message.html'
    model = Message
    form_class = RegisterResponseForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        message = Message.objects.get(pk=self.kwargs['message_pk'])
        sender = message.sender.pk
        to = message.to.pk
        user = self.request.user.pk

        if sender != user and to != user: # Só exibir template se o usuário for o sender ou o to da mensagem
            raise PermissionDenied

        context['is_mine'] = True if message.sender.pk == self.request.user.pk else False
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

list_messages_received = ListMessagesReceivedView.as_view()
list_messages_sent = ListMessagesSentView.as_view()
register_message = RegisterMessageView.as_view()
detail_message = DetailMessageView.as_view()
