from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic import (CreateView, TemplateView, ListView,
    DetailView, UpdateView, FormView, DeleteView)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages as msgs

from core.models import Vehicle
from .models import Student, Employee
from .forms import RegisterSecretaryForm, RegisterStudentForm, RegisterInstructorForm

from rolepermissions.mixins import HasPermissionsMixin
from rolepermissions.roles import assign_role

class IndexView(HasPermissionsMixin, TemplateView):
    required_permission = 'secretary'
    template_name = 'dashboard.html'

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
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        queryset = Employee.objects.all()

        if q:
            queryset = queryset.filter(name__icontains=q)
        else:
            f = self.kwargs.get('function', '')
            if f:
                queryset = queryset.filter(function=f)

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
        'salary', 'cnh', 'street', 'number', 'district', 'city', 'state']
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

class UpdateStudentView(SuccessMessageMixin, UpdateView):
    model = Student
    template_name = 'accounts/update_student.html'
    fields = ['username', 'name', 'cpf', 'date_of_birth', 'email', 'telephone',
        'street', 'number', 'district', 'city', 'state']
    success_url = reverse_lazy('accounts:list_students')
    success_message = 'Aluno atualizado com sucesso'

class StudentsListView(ListView):
    template_name = 'accounts/list_students.html'
    context_object_name = 'students'
    model = Student
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        queryset = Student.objects.all()

        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset

class DeleteStudentView(DeleteView):
    model = Student
    template_name = 'accounts/student_confirm_delete.html'
    success_url = reverse_lazy('accounts:list_students')

    def delete(self, request, *args, **kwargs):
        msgs.success(request, 'Aluno {} removido com sucesso'.format(self.get_object()))
        return super().delete(request, *args, **kwargs)

class UpdateView(SuccessMessageMixin, UpdateView):
    model = Employee
    template_name = 'accounts/update.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'salary']
    success_url = reverse_lazy('accounts:index')
    success_message = 'Dados atualizados com sucesso'

    def get_object(self):
        return self.request.user

class UpdatePasswordView(SuccessMessageMixin, FormView):
    template_name = 'accounts/update_password.html'
    success_url = reverse_lazy('logout')
    form_class = PasswordChangeForm
    success_message = 'Senha atualizada com sucesso. Realize login novamente!'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(UpdatePasswordView, self).form_valid(form)

class ChooseRegisterEmployeeView(TemplateView):
    template_name = 'accounts/register_type_employee.html'

index = IndexView.as_view()

delete_employee = DeleteEmployeeView.as_view()
list_employees = EmployeesListView.as_view()
choose_register_employee = ChooseRegisterEmployeeView.as_view()

register_secretary = RegisterSecretaryView.as_view()
update_secretary = UpdateSecretaryView.as_view()

register_instructor = RegisterInstructorView.as_view()
update_instructor = UpdateInstructorView.as_view()

register_student = RegisterStudentView.as_view()
update_student = UpdateStudentView.as_view()
list_students = StudentsListView.as_view()
delete_student = DeleteStudentView.as_view()

update = UpdateView.as_view()
update_password = UpdatePasswordView.as_view()
