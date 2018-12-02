from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from core.views.generics import ListView, CreateView, DeleteView

from process.models import PracticalClass, PracticalCourse, Process
from process.forms import RegisterPracticalClassForm, RegisterPracticalClassFormInstructor
from accounts.models import Person

from rolepermissions.mixins import HasPermissionsMixin

''' View para registro de aula prática pelo secretário '''
class RegisterPracticalClassView(HasPermissionsMixin, SuccessMessageMixin, CreateView):
    required_permission = 'secretary'
    model = PracticalClass
    template_name = 'process/register_practical_class.html'
    success_message = 'Aula registrada com sucesso'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        process = get_object_or_404(Process, practical_course__pk=self.kwargs['pk_course'])
        context['pk_process'] = process.pk
        context['instructor'] = False
        return context

    def get_success_url(self):
        return self.object.practical_course.get_absolute_url()

    def get_form(self):
        return RegisterPracticalClassForm(**self.get_form_kwargs(), argumentos=self.kwargs)

    def form_valid(self, form):
        course = get_object_or_404(PracticalCourse, pk=self.kwargs['pk_course'])
        self.object = form.save(commit=False)
        self.object.practical_course = course
        self.object.save()
        return super().form_valid(form)

''' View para registro de aula prática pelo instrutor '''
class RegisterPracticalClassViewInstructor(HasPermissionsMixin, SuccessMessageMixin, CreateView):
    required_permission = 'instructor'
    model = PracticalClass
    template_name = 'process/register_practical_class.html'
    success_message = 'Aula registrada com sucesso'
    success_url = reverse_lazy('accounts:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instructor'] = True
        return context

    def get_form(self):
        return RegisterPracticalClassFormInstructor(**self.get_form_kwargs(), argumentos=self.kwargs)

    def form_valid(self, form):
        process = form.cleaned_data['process']
        self.object = form.save(commit=False)
        self.object.practical_course = process.practical_course
        self.object.instructor = Person.objects.get(pk=self.request.user.pk)
        self.object.save()
        return super().form_valid(form)

''' Lista as aulas práticas de um determinado processo '''
class ListPracticalCourse(HasPermissionsMixin, ListView):
    required_permission = 'student'
    template_name = 'process/practicals_classes.html'

    def get_queryset(self):
        return PracticalClass.objects.filter(practical_course__process__pk=self.kwargs['pk_process'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_process'] = self.kwargs['pk_process']
        context['practical_course'] = get_object_or_404(PracticalCourse, process__pk=self.kwargs['pk_process'])

        context['classes_car'] = self.get_queryset().filter(simulator=False)
        context['classes_simulator'] = self.get_queryset().filter(simulator=True)
        return context

''' Remove uma aula prática '''
class RemovePracticalClassView(HasPermissionsMixin, DeleteView):
    required_permission = 'secretary'
    template_name = 'process/class_confirm_delete.html'

    def get_object(self):
        return get_object_or_404(PracticalClass, pk=self.kwargs['pk_class'])

    def get_success_url(self):
        messages.success(self.request, 'Aula excluída com sucesso')
        return self.object.practical_course.get_absolute_url()

practical_course = ListPracticalCourse.as_view()
register_practical_class = RegisterPracticalClassView.as_view()
remove_practical_class = RemovePracticalClassView.as_view()

register_practical_class_instructor = RegisterPracticalClassViewInstructor.as_view()
