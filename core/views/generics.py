from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView, TemplateView, FormView
from django.shortcuts import get_object_or_404
from accounts.models import Person
from core.constantes import *

class FormView(FormView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        person = get_object_or_404(Person, pk=self.request.user.pk)

        if person.current_view == SECRETARY:
            context['template_base'] = 'dashboard-secretary.html'
        elif person.current_view == ADMIN:
            context['template_base'] = 'dashboard-admin.html'
        elif person.current_view == INSTRUCTOR:
            context['template_base'] = 'dashboard-instructor.html'
        return context

class TemplateView(TemplateView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        person = get_object_or_404(Person, pk=self.request.user.pk)

        if person.current_view == SECRETARY:
            context['template_base'] = 'dashboard-secretary.html'
        elif person.current_view == ADMIN:
            context['template_base'] = 'dashboard-admin.html'
        elif person.current_view == INSTRUCTOR:
            context['template_base'] = 'dashboard-instructor.html'
        return context

class CreateView(CreateView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        person = get_object_or_404(Person, pk=self.request.user.pk)

        if person.current_view == SECRETARY:
            context['template_base'] = 'dashboard-secretary.html'
        elif person.current_view == ADMIN:
            context['template_base'] = 'dashboard-admin.html'
        elif person.current_view == INSTRUCTOR:
            context['template_base'] = 'dashboard-instructor.html'
        return context

class UpdateView(UpdateView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        person = get_object_or_404(Person, pk=self.request.user.pk)

        if person.current_view == SECRETARY:
            context['template_base'] = 'dashboard-secretary.html'
        elif person.current_view == ADMIN:
            context['template_base'] = 'dashboard-admin.html'
        elif person.current_view == INSTRUCTOR:
            context['template_base'] = 'dashboard-instructor.html'
        return context

class ListView(ListView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        person = get_object_or_404(Person, pk=self.request.user.pk)

        if person.current_view == SECRETARY:
            context['template_base'] = 'dashboard-secretary.html'
        elif person.current_view == ADMIN:
            context['template_base'] = 'dashboard-admin.html'
        elif person.current_view == INSTRUCTOR:
            context['template_base'] = 'dashboard-instructor.html'
        return context

class DeleteView(DeleteView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        person = get_object_or_404(Person, pk=self.request.user.pk)

        if person.current_view == SECRETARY:
            context['template_base'] = 'dashboard-secretary.html'
        elif person.current_view == ADMIN:
            context['template_base'] = 'dashboard-admin.html'
        elif person.current_view == INSTRUCTOR:
            context['template_base'] = 'dashboard-instructor.html'
        return context

class DetailView(DetailView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        person = get_object_or_404(Person, pk=self.request.user.pk)

        if person.current_view == SECRETARY:
            context['template_base'] = 'dashboard-secretary.html'
        elif person.current_view == ADMIN:
            context['template_base'] = 'dashboard-admin.html'
        elif person.current_view == INSTRUCTOR:
            context['template_base'] = 'dashboard-instructor.html'
        return context
