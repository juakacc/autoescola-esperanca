from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, DeleteView

from process.models import TheoreticalCourse, TheoreticalClass
from process.forms import RegisterTheoreticalClassForm
from accounts.models import Person
from core.constantes import *

from rolepermissions.mixins import HasPermissionsMixin

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

        person = get_object_or_404(Person, pk=self.request.user.pk)
        if person.current_view == SECRETARY:
            context['template_base'] = 'dashboard-secretary.html'
        elif person.current_view == ADMIN:
            context['template_base'] = 'dashboard-admin.html'

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

        person = get_object_or_404(Person, pk=self.request.user.pk)
        if person.current_view == SECRETARY:
            context['template_base'] = 'dashboard-secretary.html'
        elif person.current_view == ADMIN:
            context['template_base'] = 'dashboard-admin.html'

        return context

    def get_success_url(self):
        return self.object.theoretical_course.get_absolute_url()

    def form_valid(self, form):
        course = get_object_or_404(TheoreticalCourse, pk=self.kwargs['pk_course'])
        self.object = form.save(commit=False)
        self.object.theoretical_course = course
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        person = get_object_or_404(Person, pk=self.request.user.pk)

        if person.current_view == SECRETARY:
            context['template_base'] =  'dashboard-secretary.html'
        elif person.current_view == ADMIN:
            context['template_base'] =  'dashboard-admin.html'
        return context

theoretical_course = ListTheoreticalCourse.as_view()
register_theoretical_class = RegisterTheoreticalClass.as_view()
remove_theoretical_class = RemoveTheoreticalClassView.as_view()
