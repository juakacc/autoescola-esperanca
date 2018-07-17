from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic import (CreateView, TemplateView, ListView,
    DetailView, UpdateView, FormView, DeleteView)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages as msgs
from core.models import Student, Employee, Contact
from .models import Vehicle
from .forms import RegisterSecretaryForm, RegisterStudentForm, RegisterInstructorForm

from rolepermissions.mixins import HasPermissionsMixin
from rolepermissions.roles import assign_role

class IndexView(HasPermissionsMixin, TemplateView):
    required_permission = 'secretary'
    template_name = 'accounts/dashboard.html'

class VehiclesListView(HasPermissionsMixin, ListView):
    # required_permission = 'secretary'
    template_name = 'accounts/list_vehicles.html'
    context_object_name = 'vehicles'
    model = Vehicle

    def get_queryset(self):
        type = self.kwargs.get('type', '')
        print('a' + type)
        if type:
            query = Vehicle.objects.filter(type=type)
        else:
            query = Vehicle.objects.all()
        return query

class MessagesView(HasPermissionsMixin, ListView):
    # required_permission = 'secretary'
    template_name = 'accounts/messages.html'
    context_object_name = 'contacts'
    model = Contact

class MessageView(HasPermissionsMixin, DetailView):
    # required_permission = 'secretary'
    template_name = 'accounts/message.html'
    model = Contact

    def get_context_data(self, **kwargs):
        # Tornando a msg lida
        context = super(DetailView, self).get_context_data(**kwargs)
        message = get_object_or_404(Contact, pk=self.kwargs['pk'])
        message.visualized = True
        message.save()
        return context

class RegisterSecretaryView(SuccessMessageMixin, CreateView):
    model = Employee
    template_name = 'accounts/register_secretary.html'
    form_class = RegisterSecretaryForm
    success_url = reverse_lazy('accounts:list_employees')
    success_message = 'Secretário adicionado com sucesso'

    def get_success_url(self):
        secretary = self.object
        assign_role(secretary, 'secretary')
        secretary.function = 'secretario'
        secretary.save()
        return super(CreateView, self).get_success_url()

class EmployeesListView(ListView):
    template_name = 'accounts/list_employees.html'
    context_object_name = 'secretaries'
    model = Employee

    def get_queryset(self):
        f = self.kwargs.get('function', '')
        if f:
            queryset = Employee.objects.filter(function=f)
        else:
            queryset = Employee.objects.all()
        return queryset

class RegisterInstructorView(SuccessMessageMixin, CreateView):
    model = Employee
    template_name = 'accounts/register_instructor.html'
    form_class = RegisterInstructorForm
    success_url = reverse_lazy('accounts:list_employees')
    success_message = 'Instrutor adicionado com sucesso'

    def get_success_url(self):
        instrutor = self.object
        instrutor.function = 'instrutor'
        instrutor.save()
        # assign_role(instrutor, 'instrutor')
        return super(CreateView, self).get_success_url()

class UpdateInstructorView(SuccessMessageMixin, UpdateView):
    model = Employee
    template_name = 'accounts/update_employee.html'
    fields = ['username', 'name', 'cpf', 'date_of_birth', 'email', 'telephone',
        'salary', 'cnh', 'type_cnh', 'street', 'number', 'district', 'city', 'state']
    success_url = reverse_lazy('accounts:list_employees')
    success_message = 'Instrutor atualizado com sucesso'

class DeleteEmployeeView(DeleteView):
    model = Employee
    template_name = 'accounts/employee_confirm_delete.html'
    success_url = reverse_lazy('accounts:list_employees')

    def delete(self, request, *args, **kwargs):
        msgs.success(request, 'Funcionário {} removido com sucesso'.format(self.get_object()))
        return super(DeleteEmployeeView, self).delete(request, *args, **kwargs)

class UpdateSecretaryView(SuccessMessageMixin, UpdateView):
    model = Employee
    template_name = 'accounts/update_employee.html'
    fields = ['name', 'cpf', 'date_of_birth', 'email', 'telephone', 'salary',
        'street', 'number', 'district', 'city', 'state']
    success_url = reverse_lazy('accounts:list_employees')
    success_message = 'Secretário atualizado com sucesso'

class RegisterStudentView(SuccessMessageMixin, CreateView):
    model = Student
    template_name = 'accounts/register_student.html'
    form_class = RegisterStudentForm
    success_url = reverse_lazy('accounts:list_students')
    success_message = 'Aluno adicionado com sucesso'

class StudentsListView(ListView):
    template_name = 'accounts/list_students.html'
    context_object_name = 'students'
    model = Student

class RegisterVehicleView(SuccessMessageMixin, CreateView):
    model = Vehicle
    template_name = 'accounts/register_vehicle.html'
    fields = '__all__'
    success_url = reverse_lazy('accounts:list_vehicles')
    success_message = 'Veículo adicionado com sucesso'

class UpdateVehicleView(SuccessMessageMixin, UpdateView):
    model = Vehicle
    template_name = 'accounts/update_vehicle.html'
    fields = ['fabricator', 'model', 'year', 'plate', 'state']
    success_url = reverse_lazy('accounts:list_vehicles')
    success_message = 'Veículo atualizado com sucesso'

class DeleteVehicleView(DeleteView):
    model = Vehicle
    success_url = reverse_lazy('accounts:list_vehicles')

    def delete(self, request, *args, **kwargs):
        msgs.success(request, 'Veículo removido com sucesso')
        return super(DeleteVehicleView, self).delete(request, *args, **kwargs)

class UpdateView(SuccessMessageMixin, UpdateView):
    model = Employee
    template_name = 'accounts/update.html'
    fields = ['first_name', 'last_name', 'email', 'salary']
    success_url = reverse_lazy('accounts:index')
    success_message = 'Dados atualizados com sucesso'

    def get_object(self):
        return self.request.user.employee

class UpdatePasswordView(SuccessMessageMixin, FormView):
    template_name = 'accounts/update_password.html'
    success_url = reverse_lazy('logout')
    form_class = PasswordChangeForm
    success_message = 'Senha atualizada com sucesso. Realize login novamente!'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user.employee
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(UpdatePasswordView, self).form_valid(form)

index = IndexView.as_view()

messages = MessagesView.as_view()
message = MessageView.as_view()

delete_employee = DeleteEmployeeView.as_view()
list_employees = EmployeesListView.as_view()

register_secretary = RegisterSecretaryView.as_view()
update_secretary = UpdateSecretaryView.as_view()

register_instructor = RegisterInstructorView.as_view()
update_instructor = UpdateInstructorView.as_view()

register_student = RegisterStudentView.as_view()
list_students = StudentsListView.as_view()

register_vehicle = RegisterVehicleView.as_view()
update_vehicle = UpdateVehicleView.as_view()
delete_vehicle = DeleteVehicleView.as_view()
list_vehicles = VehiclesListView.as_view()

update = UpdateView.as_view()
update_password = UpdatePasswordView.as_view()
