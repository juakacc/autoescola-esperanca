from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Contact, Vehicle, SystemSettings
from .forms import ResponseContactForm, RegisterVehicleForm

from rolepermissions.mixins import HasPermissionsMixin

class RegisterVehicleView(SuccessMessageMixin, CreateView):
    model = Vehicle
    template_name = 'accounts/register_vehicle.html'
    form_class = RegisterVehicleForm
    success_url = reverse_lazy('accounts:list_vehicles')
    success_message = 'Veículo adicionado com sucesso'

class UpdateVehicleView(SuccessMessageMixin, UpdateView):
    model = Vehicle
    template_name = 'accounts/update_vehicle.html'
    fields = ['slug', 'fabricator', 'model', 'year', 'plate', 'state']
    success_url = reverse_lazy('accounts:list_vehicles')
    success_message = 'Veículo atualizado com sucesso'

class DeleteVehicleView(DeleteView):
    model = Vehicle
    success_url = reverse_lazy('accounts:list_vehicles')

    def delete(self, request, *args, **kwargs):
        msgs.success(request, 'Veículo removido com sucesso')
        return super(DeleteVehicleView, self).delete(request, *args, **kwargs)

class VehiclesListView(HasPermissionsMixin, ListView):
    # required_permission = 'secretary'
    template_name = 'accounts/list_vehicles.html'
    context_object_name = 'vehicles'
    model = Vehicle
    paginate_by = 10

    def get_queryset(self):
        type = self.kwargs.get('type', '')
        if type:
            query = Vehicle.objects.filter(type=type)
        else:
            query = Vehicle.objects.all()
        return query

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

class UpdateSettingsView(SuccessMessageMixin, UpdateView):
    model = SystemSettings
    template_name = 'update_settings.html'
    fields = '__all__'
    success_url = reverse_lazy('accounts:index')
    success_message = 'Configurações atualizadas com sucesso'

    def get_object(self):
        return SystemSettings.objects.all()[0]

class QuemSomosView(TemplateView):
    template_name = 'quem_somos.html'


contact = ContactView.as_view()
messages = MessagesView.as_view()
message = MessageView.as_view()

update_settings = UpdateSettingsView.as_view()

quem_somos = QuemSomosView.as_view()

register_vehicle = RegisterVehicleView.as_view()
update_vehicle = UpdateVehicleView.as_view()
delete_vehicle = DeleteVehicleView.as_view()
list_vehicles = VehiclesListView.as_view()
