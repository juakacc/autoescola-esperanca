from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.urls import reverse_lazy

from accounts.models import Person
from accounts.forms import RegisterStudentForm

from rolepermissions.mixins import HasPermissionsMixin
from rolepermissions.roles import assign_role

class RegisterStudentView(HasPermissionsMixin, SuccessMessageMixin, CreateView):
    required_permission = 'secretary'
    model = Person
    template_name = 'accounts/register_student.html'
    form_class = RegisterStudentForm
    success_url = reverse_lazy('accounts:list_students')
    success_message = 'Aluno adicionado com sucesso'

    def get_success_url(self):
        student = self.object
        assign_role(student, 'student')
        student.role_student = True
        student.save()
        return super().get_success_url()

class UpdateStudentView(SuccessMessageMixin, UpdateView):
    model = Person
    template_name = 'accounts/update_student.html'
    fields = ['username', 'name', 'cpf', 'date_of_birth', 'email', 'telephone',
        'street', 'number', 'district', 'city', 'state']
    success_url = reverse_lazy('accounts:list_students')
    success_message = 'Aluno atualizado com sucesso'

class ListStudentsView(ListView):
    template_name = 'accounts/list_students.html'
    context_object_name = 'students'
    # model = Person
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        queryset = Person.objects.filter(role_student=True)

        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset

class DetailStudentView(DetailView):
    model = Person

class DeleteStudentView(DeleteView):
    model = Person
    template_name = 'accounts/student_confirm_delete.html'
    success_url = reverse_lazy('accounts:list_students')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Aluno {} removido com sucesso'.format(self.get_object()))
        return super().delete(request, *args, **kwargs)

register_student = RegisterStudentView.as_view()
update_student = UpdateStudentView.as_view()
list_students = ListStudentsView.as_view()
detail_student = DetailStudentView.as_view()
delete_student = DeleteStudentView.as_view()
