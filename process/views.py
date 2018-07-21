from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from .models import Process, Exam, TheoreticalClass, TheoreticalCourse
from .forms import RegisterProcessForm, RegisterClassForm

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

class ExamsUpdateView(SuccessMessageMixin, UpdateView):
    model = Exam
    template_name = 'process/update_exams.html'
    fields = ['exam_medical', 'exam_psychological']
    # success_url = reverse_lazy('process:detail_process', kwargs={'pk': self.request.kwargs['pk']})
    success_message = 'Exames atualizados com sucesso'

    def get_success_url(self, **kwargs):
        return self.object.process.get_absolute_url()

    def get_object(self):
        exams = get_object_or_404(Process, pk=self.kwargs['pk']).exams
        return exams

class ListTheoreticalCourse(ListView):
    model = TheoreticalClass
    template_name = 'process/theoreticals_classes.html'
    context_object_name = 'classes'

    def get_queryset(self):
        return TheoreticalClass.objects.filter(theoretical_course=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        process = get_object_or_404(Process, pk=self.kwargs['pk'])
        context['theoretical_course'] = process.theoretical_course
        return context

class RegisterClass(SuccessMessageMixin, CreateView):
    model = TheoreticalClass
    form_class = RegisterClassForm
    template_name = 'process/register_class.html'
    success_url = reverse_lazy('process:list_processes')
    success_message = 'Aula registrada com sucesso'

    def form_valid(self, form):
        course = get_object_or_404(TheoreticalCourse, pk=self.kwargs['pk'])
        self.object = form.save(commit=False)
        self.object.theoretical_course = course
        self.object.save()
        return super().form_valid(form)

register_process = RegisterProcessView.as_view()
list_processes = ProcessListView.as_view()
delete_process = DeleteProcessView.as_view()
detail_process = ProcessDetailView.as_view()

register_class = RegisterClass.as_view()

update_exams = ExamsUpdateView.as_view()
theoreticals_courses = ListTheoreticalCourse.as_view()
