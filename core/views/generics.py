from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView, TemplateView, FormView
from django.views import View
from accounts.models import Person
from core.constantes import *

class Base():
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            person = Person.objects.get(pk=self.request.user.pk)

            if person.current_view == SECRETARY:
                context['template_base'] = 'dashboard-secretary.html'
            elif person.current_view == ADMIN:
                context['template_base'] = 'dashboard-admin.html'
            elif person.current_view == INSTRUCTOR:
                context['template_base'] = 'dashboard-instructor.html'
            elif person.current_view == STUDENT:
                context['template_base'] = 'dashboard-student.html'
            else:
                context['template_base'] = 'base.html'
        except:
            context['template_base'] = 'base.html'

        return context

    def get_success_url(self):
        return self.success_url or self.request.META.get('HTTP_REFERER')

class FormView(Base, FormView):
    pass

class TemplateView(Base, TemplateView):
    pass

class CreateView(Base, CreateView):
    pass

class UpdateView(Base, UpdateView):
    pass

class ListView(Base, ListView):
    pass

class DeleteView(Base, DeleteView):
    pass

class DetailView(Base, DetailView):
    pass
