from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (TemplateView, UpdateView, FormView)

from core.models import Vehicle
from accounts.models import Person

from rolepermissions.mixins import HasPermissionsMixin
from rolepermissions.checkers import has_permission, has_role

class IndexAccountView(HasPermissionsMixin, TemplateView):
    required_permission = 'student'

    def get_template_names(self):
        user = self.request.user
        if has_permission(user, 'admin'):
            return 'dashboard-admin.html'
        elif has_permission(user, 'secretary'):
            return 'dashboard-secretary.html'
        elif has_permission(user, 'instructor'):
            return 'dashboard-instructor.html'
        elif has_permission(user, 'student'):
            return 'dashboard-student.html'

class UpdateMyDataView(HasPermissionsMixin, SuccessMessageMixin, UpdateView):
    required_permission = 'student'
    template_name = 'accounts/update.html'
    # Fields de Person
    fields = ['username', 'name', 'cpf', 'email', 'date_of_birth', 'telephone', 'street', 'number', 'district', 'city', 'state']
    success_url = reverse_lazy('accounts:index')
    success_message = 'Dados atualizados com sucesso'

    def get_object(self):
        user = self.request.user
        if has_role(user, 'instructor'):
            self.fields += ['cnh']
            return Employee.objects.get(pk=user.pk)
        return Person.objects.get(pk=user.pk)

class UpdateMyPasswordView(SuccessMessageMixin, FormView):
    template_name = 'accounts/update_password.html'
    success_url = reverse_lazy('core:logout')
    form_class = PasswordChangeForm
    success_message = 'Senha atualizada com sucesso. Realize login novamente!'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(UpdatePasswordView, self).form_valid(form)

index = IndexAccountView.as_view()
update_data = UpdateMyDataView.as_view()
update_password = UpdateMyPasswordView.as_view()
