from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from core.views.generics import (TemplateView, UpdateView, FormView)

from core.models import Vehicle
from core.constantes import *
from accounts.models import Person, PasswordReset
from accounts.forms import PasswordResetForm

from rolepermissions.mixins import HasPermissionsMixin
from rolepermissions.checkers import has_permission, has_role

class IndexAccountView(HasPermissionsMixin, TemplateView):
    required_permission = 'student'
    template_name = 'accounts/index.html'

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

class UpdateMyPasswordView(HasPermissionsMixin, SuccessMessageMixin, FormView):
    required_permission = 'student'
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

class PasswordResetView(SuccessMessageMixin, FormView):
    template_name = 'accounts/password_reset.html'
    form_class = PasswordResetForm
    success_message = 'Um e-mail foi enviado para você'
    success_url = reverse_lazy('accounts:reset_password')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class PasswordResetConfirmView(SuccessMessageMixin, FormView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_message = 'Senha redefinida com sucesso'
    success_url = reverse_lazy('core:login')

    def dispatch(self, request, *args, **kwargs):
        reset = get_object_or_404(PasswordReset, key=self.kwargs.get('key'))

        if reset.confirmed: # Esse reset já foi utilizado
            messages.warning(self.request, 'Por questões de segurança esse pedido expirou, solicite-o novamente!')
            return redirect('core:login')
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        reset = get_object_or_404(PasswordReset, key=self.kwargs.get('key'))
        kwargs['user'] = reset.user
        kwargs['data'] = self.request.POST or None
        return kwargs

    def form_valid(self, form):
        form.save()
        reset = get_object_or_404(PasswordReset, key=self.kwargs.get('key'))
        reset.confirmed = True
        reset.save()
        return super().form_valid(form)

index = IndexAccountView.as_view()
update_data = UpdateMyDataView.as_view()
update_password = UpdateMyPasswordView.as_view()

reset_password = PasswordResetView.as_view()
password_reset_confirm = PasswordResetConfirmView.as_view()
