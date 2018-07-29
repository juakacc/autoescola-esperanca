from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from accounts.models import Person
from process.models import Process
from process.forms import RegisterProcessForm
from core.views.generics import CreateView, UpdateView, ListView, DetailView, DeleteView

from rolepermissions.mixins import HasPermissionsMixin

class RegisterProcessView(HasPermissionsMixin, SuccessMessageMixin, CreateView):
    required_permission = 'secretary'
    model = Process
    form_class = RegisterProcessForm
    template_name = 'process/register_process.html'
    success_url = reverse_lazy('process:list_processes')

    def get_success_url(self):
        process = self.object
        self.success_message = 'Processo cadastrado. Prazo final {}'.format(process.end_date)
        return super().get_success_url()

class UpdateProcessView(HasPermissionsMixin, SuccessMessageMixin, UpdateView):
    required_permission = 'secretary'
    template_name = 'process/update_process.html'
    success_message = 'Processo atualizado com sucesso'
    success_url = reverse_lazy('process:list_processes')
    fields = ['type_cnh', 'begin_date']

    def get_object(self):
        return get_object_or_404(Process, pk=self.kwargs['pk_process'])

class ProcessListView(HasPermissionsMixin, ListView):
    required_permission = 'secretary'
    template_name = 'process/list_processes.html'
    pagination_by = 10
    context_object_name = 'processes'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        queryset = Process.objects.all()
        if q:
            queryset = queryset.filter(student__name__icontains=q)
        return queryset

class ProcessDetailView(DetailView):
    model = Process
    template_name = 'process/detail_process.html'

    def get_object(self, **kwargs):
        return get_object_or_404(Process, pk=self.kwargs['pk_process'])

class DeleteProcessView(HasPermissionsMixin, DeleteView):
    required_permission = 'secretary'
    model = Process
    success_url = reverse_lazy('process:list_processes')

    def delele(self, request, *args, **kwargs):
        messages.success(self.request, 'Processo removido com sucesso')
        return super().delete(request, *args, **kwargs)

class ExamsUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'process/update_exams.html'
    fields = ['exam_medical', 'exam_psychological']
    success_message = 'Exames atualizados com sucesso'

    def get_success_url(self, **kwargs):
        return self.object.process.get_absolute_url()

    def get_object(self):
        exams = get_object_or_404(Process, pk=self.kwargs['pk_process']).exams
        return exams

register_process = RegisterProcessView.as_view()
update_process = UpdateProcessView.as_view()
list_processes = ProcessListView.as_view()
delete_process = DeleteProcessView.as_view()
detail_process = ProcessDetailView.as_view()
update_exams = ExamsUpdateView.as_view()
