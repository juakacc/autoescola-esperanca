from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, DeleteView

from process.models import PracticalClass, PracticalCourse
from process.forms import RegisterPracticalClassForm
from accounts.models import Person
from core.constantes import * 

from rolepermissions.mixins import HasPermissionsMixin

class RegisterPracticalClass(SuccessMessageMixin, CreateView):
    model = PracticalClass
    form_class = RegisterPracticalClassForm
    template_name = 'process/register_practical_class.html'
    success_message = 'Aula registrada com sucesso'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        process = get_object_or_404(Process, practical_course__pk=self.kwargs['pk_course'])
        context['pk_process'] = process.pk

        person = get_object_or_404(Person, pk=self.request.user.pk)
        if person.current_view == SECRETARY:
            context['template_base'] = 'dashboard-secretary.html'
        elif person.current_view == ADMIN:
            context['template_base'] = 'dashboard-admin.html'

        return context

    def get_success_url(self):
        return self.object.practical_course.get_absolute_url()

    def form_valid(self, form):
        course = get_object_or_404(PracticalCourse, pk=self.kwargs['pk_course'])
        self.object = form.save(commit=False)
        self.object.practical_course = course
        self.object.save()
        return super().form_valid(form)

class ListPracticalCourse(ListView):
    model = PracticalClass
    template_name = 'process/practicals_classes.html'

    def get_queryset(self):
        return PracticalClass.objects.filter(practical_course__process__pk=self.kwargs['pk_process'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_process'] = self.kwargs['pk_process']
        context['practical_course'] = get_object_or_404(PracticalCourse, process__pk=self.kwargs['pk_process'])

        context['classes_car'] = self.get_queryset().filter(simulator=False)
        context['classes_simulator'] = self.get_queryset().filter(simulator=True)

        person = get_object_or_404(Person, pk=self.request.user.pk)
        if person.current_view == SECRETARY:
            context['template_base'] = 'dashboard-secretary.html'
        elif person.current_view == ADMIN:
            context['template_base'] = 'dashboard-admin.html'

        return context

class RemovePracticalClassView(DeleteView):
    model = PracticalClass
    template_name = 'process/class_confirm_delete.html'

    def get_object(self):
        return get_object_or_404(PracticalClass, pk=self.kwargs['pk_class'])

    def get_success_url(self):
        messages.success(self.request, 'Aula excluída com sucesso')
        return self.object.practical_course.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        person = get_object_or_404(Person, pk=self.request.user.pk)
        if person.current_view == SECRETARY:
            context['template_base'] = 'dashboard-secretary.html'
        elif person.current_view == ADMIN:
            context['template_base'] = 'dashboard-admin.html'
        return context

practical_course = ListPracticalCourse.as_view()
register_practical_class = RegisterPracticalClass.as_view()
remove_practical_class = RemovePracticalClassView.as_view()
