from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from core.views.generics import ListView, CreateView, DeleteView

from process.models import TheoreticalCourse, TheoreticalClass, Process
from process.forms import RegisterTheoreticalClassForm, RegisterTheoreticalClassFormInstructor
from accounts.models import Person

from rolepermissions.mixins import HasPermissionsMixin

''' Listagem das aulas teóricas de um determinado processo '''
class ListTheoreticalCourse(HasPermissionsMixin, ListView):
    required_permission = 'student'
    template_name = 'process/theoreticals_classes.html'
    context_object_name = 'classes'

    def get_queryset(self):
        return TheoreticalClass.objects.filter(theoretical_course__process__pk=self.kwargs['pk_process'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_process'] = self.kwargs['pk_process']
        context['theoretical_course'] = get_object_or_404(TheoreticalCourse, process__pk=self.kwargs['pk_process'])
        return context

''' View para registro de aula teórica pelo secretário '''
class RegisterTheoreticalClassView(HasPermissionsMixin, SuccessMessageMixin, CreateView):
    required_permission = 'secretary'
    model = TheoreticalClass
    form_class = RegisterTheoreticalClassForm
    template_name = 'process/register_theoretical_class.html'
    success_message = 'Aula registrada com sucesso'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        process = get_object_or_404(Process, theoretical_course__pk=self.kwargs['pk_course'])
        context['pk_process'] = process.pk
        context['instructor'] = False
        return context

    def get_success_url(self):
        return self.object.theoretical_course.get_absolute_url()

    def form_valid(self, form):
        course = get_object_or_404(TheoreticalCourse, pk=self.kwargs['pk_course'])
        self.object = form.save(commit=False)
        self.object.theoretical_course = course
        self.object.save()
        return super().form_valid(form)

''' View para registro de aula teórica pelo Instrutor '''
class RegisterTheoreticalClassViewInstructor(HasPermissionsMixin, SuccessMessageMixin, CreateView):
    required_permission = 'instructor'
    model  = TheoreticalClass
    form_class = RegisterTheoreticalClassFormInstructor
    template_name = 'process/register_theoretical_class.html'
    success_message = 'Aula registrada com sucesso'
    success_url = reverse_lazy('accounts:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instructor'] = True
        return context

    def form_valid(self, form):
        process = form.cleaned_data['process']
        self.object = form.save(commit=False)
        self.object.theoretical_course = process.theoretical_course
        self.object.instructor = Person.objects.get(pk=self.request.user.pk)
        self.object.save()
        return super().form_valid(form)

''' View para remoção de aula teórica '''
class RemoveTheoreticalClassView(HasPermissionsMixin, DeleteView):
    required_permission = 'secretary'
    template_name = 'process/class_confirm_delete.html'

    def get_object(self):
        return get_object_or_404(TheoreticalClass, pk=self.kwargs['pk_class'])

    def get_success_url(self):
        messages.success(self.request, 'Aula excluída com sucesso')
        return self.object.theoretical_course.get_absolute_url()

theoretical_course = ListTheoreticalCourse.as_view()
register_theoretical_class = RegisterTheoreticalClassView.as_view()
remove_theoretical_class = RemoveTheoreticalClassView.as_view()

register_theoretical_class_instructor = RegisterTheoreticalClassViewInstructor.as_view()
