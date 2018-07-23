from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import (Process, Exam, TheoreticalClass,
    TheoreticalCourse, PracticalCourse, PracticalClass)
from .forms import RegisterProcessForm, RegisterTheoreticalClassForm, RegisterPracticalClassForm

class RegisterProcessView(SuccessMessageMixin, CreateView):
    model = Process
    form_class = RegisterProcessForm
    template_name = 'process/register_process.html'
    success_url = reverse_lazy('process:list_processes')

    def get_success_url(self):
        process = self.object
        self.success_message = 'Processo cadastrado. Prazo final {}'.format(process.date_end)
        return super().get_success_url()

class UpdateProcessView(SuccessMessageMixin, UpdateView):
    model = Process
    template_name = 'process/update_process.html'
    success_message = 'Processo atualizado com sucesso'
    success_url = reverse_lazy('process:list_processes')
    fields = ['type_cnh', 'date_start']

    def get_object(self):
        return get_object_or_404(Process, pk=self.kwargs['pk_process'])

class ProcessListView(ListView):
    model = Process
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

class DeleteProcessView(DeleteView):
    model = Process
    success_url = reverse_lazy('process:list_processes')

    def delele(self, request, *args, **kwargs):
        messages.success(self.request, 'Processo removido com sucesso')
        return super().delete(request, *args, **kwargs)

class ExamsUpdateView(SuccessMessageMixin, UpdateView):
    model = Exam
    template_name = 'process/update_exams.html'
    fields = ['exam_medical', 'exam_psychological']
    success_message = 'Exames atualizados com sucesso'

    def get_success_url(self, **kwargs):
        return self.object.process.get_absolute_url()

    def get_object(self):
        exams = get_object_or_404(Process, pk=self.kwargs['pk_process']).exams
        return exams

class ListTheoreticalCourse(ListView):
    model = TheoreticalClass
    template_name = 'process/theoreticals_classes.html'
    context_object_name = 'classes'

    def get_queryset(self):
        return TheoreticalClass.objects.filter(theoretical_course__process__pk=self.kwargs['pk_process'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_process'] = self.kwargs['pk_process']
        context['theoretical_course'] = get_object_or_404(TheoreticalCourse, process__pk=self.kwargs['pk_process'])
        return context

class ListPracticalCourse(ListView):
    model = PracticalClass
    template_name = 'process/practicals_classes.html'

    def get_queryset(self):
        return PracticalClass.objects.filter(practical_course__process__pk=self.kwargs['pk_process'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_process'] = self.kwargs['pk_process']
        context['practical_course'] = get_object_or_404(PracticalCourse, process__pk=self.kwargs['pk_process'])

        context['classes_car'] = PracticalClass.objects.filter(simulator=False)
        context['classes_simulator'] = PracticalClass.objects.filter(simulator=True)
        return context

class RegisterTheoreticalClass(SuccessMessageMixin, CreateView):
    model = TheoreticalClass
    form_class = RegisterTheoreticalClassForm
    template_name = 'process/register_theoretical_class.html'
    success_message = 'Aula registrada com sucesso'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        process = get_object_or_404(Process, theoretical_course__pk=self.kwargs['pk_course'])
        context['pk_process'] = process.pk
        return context

    def get_success_url(self):
        return self.object.theoretical_course.get_absolute_url()

    def form_valid(self, form):
        course = get_object_or_404(TheoreticalCourse, pk=self.kwargs['pk_course'])
        self.object = form.save(commit=False)
        self.object.theoretical_course = course
        self.object.save()
        return super().form_valid(form)

class RegisterPracticalClass(SuccessMessageMixin, CreateView):
    model = PracticalClass
    form_class = RegisterPracticalClassForm
    template_name = 'process/register_practical_class.html'
    success_message = 'Aula registrada com sucesso'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        process = get_object_or_404(Process, practical_course__pk=self.kwargs['pk_course'])
        context['pk_process'] = process.pk
        return context

    def get_success_url(self):
        return self.object.practical_course.get_absolute_url()

    def form_valid(self, form):
        course = get_object_or_404(PracticalCourse, pk=self.kwargs['pk_course'])
        self.object = form.save(commit=False)
        self.object.practical_course = course
        self.object.save()
        return super().form_valid(form)

class RemoveTheoreticalClassView(DeleteView):
    model = TheoreticalClass
    template_name = 'process/class_confirm_delete.html'

    def get_object(self):
        return get_object_or_404(TheoreticalClass, pk=self.kwargs['pk_class'])

    def get_success_url(self):
        messages.success(self.request, 'Aula excluída com sucesso')
        return self.object.theoretical_course.get_absolute_url()

class RemovePracticalClassView(DeleteView):
    model = PracticalClass
    template_name = 'process/class_confirm_delete.html'

    def get_object(self):
        return get_object_or_404(PracticalClass, pk=self.kwargs['pk_class'])

    def get_success_url(self):
        messages.success(self.request, 'Aula excluída com sucesso')
        return self.object.practical_course.get_absolute_url()

register_process = RegisterProcessView.as_view()
update_process = UpdateProcessView.as_view()
list_processes = ProcessListView.as_view()
delete_process = DeleteProcessView.as_view()
detail_process = ProcessDetailView.as_view()

register_theoretical_class = RegisterTheoreticalClass.as_view()
remove_theoretical_class = RemoveTheoreticalClassView.as_view()

register_practical_class = RegisterPracticalClass.as_view()
remove_practical_class = RemovePracticalClassView.as_view()

update_exams = ExamsUpdateView.as_view()
theoretical_course = ListTheoreticalCourse.as_view()
practical_course = ListPracticalCourse.as_view()
