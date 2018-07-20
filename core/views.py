from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import Contact
from .forms import ResponseContactForm

from rolepermissions.mixins import HasPermissionsMixin

def index(request):
    return render(request, 'base.html')

class MessagesView(HasPermissionsMixin, ListView):
    # required_permission = 'secretary'
    template_name = 'list_contacts.html'
    context_object_name = 'contacts'
    model = Contact
    paginate_by = 10

class MessageView(HasPermissionsMixin, UpdateView):
    # required_permission = 'secretary'
    template_name = 'detail_contact.html'
    model = Contact
    form_class = ResponseContactForm
    success_url = reverse_lazy('accounts:messages')

    def get_object(self):
        # Tornando a msg lida
        msg = super().get_object()
        msg.visualized = True
        msg.save()
        return msg

    def form_valid(self, form):
        # Enviar e-mail
        form.save()
        form.send_email(self.get_object())
        return super().form_valid(form)

class ContactView(SuccessMessageMixin, CreateView):
    template_name = 'contact.html'
    model = Contact
    success_url = reverse_lazy('index')
    fields = ['name', 'email', 'subject', 'message']

    success_message = 'Obrigado pelo contato'

contact = ContactView.as_view()
messages = MessagesView.as_view()
message = MessageView.as_view()
