from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin

from .models import Process
from .forms import RegisterProcessForm

class RegisterProcessView(SuccessMessageMixin, CreateView):
    model = Process
    form_class = RegisterProcessForm
    template_name = 'process/register_process.html'
    success_url = reverse_lazy('process:list_processes')

    def get_success_url(self):
        process = self.object
        self.success_message = 'Processo cadastrado. Prazo final {}'.format(process.date_end)
        return super().get_success_url()

class ProcessListView(ListView):
    model = Process
    template_name = 'process/list_processes.html'
    pagination_by = 10
    context_object_name = 'processes'

class ProcessDetailView(DetailView):
    model = Process
    template_name = 'process/detail_process.html'

class DeleteProcessView(SuccessMessageMixin, DeleteView):
    model = Process
    success_url = reverse_lazy('process:list_processes')

    def delele(self, request, *args, **kwargs):
        self.success_message = 'Processo removido com sucesso'
        return super().delete(request, *args, **kwargs)

register_process = RegisterProcessView.as_view()
list_processes = ProcessListView.as_view()
delete_process = DeleteProcessView.as_view()
detail_process = ProcessDetailView.as_view()
