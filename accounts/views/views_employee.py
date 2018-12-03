from django.contrib import messages as msgs
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from accounts.models import Person
from accounts.forms import RegisterEmployeeForm, UpdateEmployeeForm
from core.constantes import *
from core.views.generics import CreateView, UpdateView, ListView, DeleteView, DetailView, TemplateView

from rolepermissions.roles import assign_role
from rolepermissions.mixins import HasPermissionsMixin

class RegisterEmployeeView(HasPermissionsMixin, SuccessMessageMixin, CreateView):
    required_permission = 'secretary'
    model = Person
    template_name = 'accounts/register_employee.html'
    form_class = RegisterEmployeeForm
    success_url = reverse_lazy('accounts:list_employees')
    success_message = 'Funcionário adicionado com sucesso'

    def get_success_url(self):
        func = self.object
        if func.role_secretary:
            assign_role(func, 'secretary')
        if func.role_instructor:
            assign_role(func, 'instructor')
        if func.role_admin:
            assign_role(func, 'admin')
        func.save()
        return super().get_success_url()

class UpdateEmployeeView(HasPermissionsMixin, SuccessMessageMixin, UpdateView):
    required_permission = 'secretary'
    model = Person
    template_name = 'accounts/update_employee.html'
    form_class = UpdateEmployeeForm
    success_url = reverse_lazy('accounts:list_employees')
    success_message = 'Funcionário atualizado com sucesso'

class DetailEmployeeView(HasPermissionsMixin, DetailView):
    required_permission = 'secretary'
    model = Person
    context_object_name = 'aluno'
    template_name = 'accounts/person_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['person_func'] = True
        return context

class EmployeesListView(HasPermissionsMixin, ListView):
    required_permission = 'student'
    template_name = 'accounts/list_employees.html'
    context_object_name = 'secretaries'
    model = Person
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        person = Person.objects.get(pk=self.request.user.pk)
        context['is_aluno'] = person.current_view == 'aluno'
        return context

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        queryset = Person.objects.all() # Colocar o OR

        if q:
            queryset = queryset.filter(name__icontains=q)
        else:
            f = self.kwargs.get('function', '')
            if f:
                if f == 'secretario':
                    queryset = queryset.filter(role_secretary=True)
                elif f == 'instrutor':
                    queryset = queryset.filter(role_instructor=True)
        return queryset

class DeleteEmployeeView(HasPermissionsMixin, DeleteView):
    required_permission = 'secretary'
    model = Person
    template_name = 'accounts/employee_confirm_delete.html'
    success_url = reverse_lazy('accounts:list_employees')

    def delete(self, request, *args, **kwargs):
        msgs.success(request, 'Funcionário {} removido com sucesso'.format(self.get_object()))
        return super().delete(request, *args, **kwargs)

delete_employee = DeleteEmployeeView.as_view()
list_employees = EmployeesListView.as_view()
detail_employee = DetailEmployeeView.as_view()
register_employee = RegisterEmployeeView.as_view()
update_employee = UpdateEmployeeView.as_view()
