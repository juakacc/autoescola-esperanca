from django.shortcuts import get_object_or_404, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from core.models import Contact, Vehicle, SystemSettings
from core.forms import ResponseContactForm, RegisterVehicleForm, UpdateSettingsForm
from core.views.generics import CreateView, ListView, UpdateView, DeleteView
from accounts.models import Person

from rolepermissions.mixins import HasPermissionsMixin

class MessagesView(HasPermissionsMixin, ListView):
    required_permission = 'secretary'
    template_name = 'list_contacts.html'
    context_object_name = 'contacts'
    model = Contact
    paginate_by = 10

class MessageView(HasPermissionsMixin, UpdateView):
    required_permission = 'secretary'
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

class UpdateSettingsView(HasPermissionsMixin, SuccessMessageMixin, UpdateView):
    required_permission = 'secretary'
    template_name = 'update_settings.html'
    model = SystemSettings
    form_class = UpdateSettingsForm
    success_url = reverse_lazy('accounts:index')
    success_message = 'Configurações atualizadas com sucesso'

    def get_object(self):
        return SystemSettings.objects.all()[0]

class RedirectHomeView(RedirectView):
    ''' Altera a view_current da pessoa e redireciona para o home apropriado '''

    def get_redirect_url(self, **kwargs):
        person = get_object_or_404(Person, pk=self.request.user.pk)
        view = kwargs['type']
        person.current_view = view
        person.save()
        return reverse_lazy('accounts:index')

messages = MessagesView.as_view()
message = MessageView.as_view()
update_settings = UpdateSettingsView.as_view()
red_home = RedirectHomeView.as_view()
