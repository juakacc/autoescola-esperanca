from django.contrib import messages as msgs
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from core.models import Vehicle
from core.forms import RegisterVehicleForm
from core.views.generics import CreateView, ListView, UpdateView, DeleteView, DetailView

from rolepermissions.mixins import HasPermissionsMixin

class RegisterVehicleView(HasPermissionsMixin, SuccessMessageMixin, CreateView):
    required_permission = 'secretary'
    model = Vehicle
    template_name = 'accounts/register_vehicle.html'
    form_class = RegisterVehicleForm
    success_url = reverse_lazy('accounts:list_vehicles')
    success_message = 'Veículo adicionado com sucesso'

class UpdateVehicleView(HasPermissionsMixin, SuccessMessageMixin, UpdateView):
    required_permission = 'secretary'
    model = Vehicle
    template_name = 'accounts/update_vehicle.html'
    fields = ['slug', 'fabricator', 'model', 'year', 'plate', 'state']
    success_url = reverse_lazy('accounts:list_vehicles')
    success_message = 'Veículo atualizado com sucesso'

class DeleteVehicleView(HasPermissionsMixin, DeleteView):
    required_permission = 'secretary'
    model = Vehicle
    template_name = 'accounts/vehicle_confirm_delete.html'
    success_url = reverse_lazy('accounts:list_vehicles')

    def delete(self, request, *args, **kwargs):
        msgs.success(request, 'Veículo removido com sucesso')
        return super().delete(request, *args, **kwargs)

class VehiclesListView(HasPermissionsMixin, ListView):
    required_permission = 'instructor'
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

class DetailVehicleView(HasPermissionsMixin, DetailView):
    required_permission = 'student'
    model = Vehicle
    template_name = 'accounts/vehicle_detail.html'

register_vehicle = RegisterVehicleView.as_view()
update_vehicle = UpdateVehicleView.as_view()
delete_vehicle = DeleteVehicleView.as_view()
list_vehicles = VehiclesListView.as_view()
detail_vehicle = DetailVehicleView.as_view()
