from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

import calendar
from datetime import datetime, timedelta

from process.models import PracticalClass, Process
from .forms import RegisterAppointmentForm, RegisterPracticalClassForm
from .models import Appointment
from core.views.generics import ListView, CreateView, DeleteView, DetailView
from accounts.models import Person

from rolepermissions.mixins import HasPermissionsMixin

class ListDiariesView(HasPermissionsMixin, ListView):
    required_permission = 'secretary'
    model = Appointment
    template_name = 'diary/list_appointments.html'
    context_object_name = 'appointments'
    paginate_by = 10

    def get_queryset(self):
        begin, end = self.request.GET.get('begin', ''), self.request.GET.get('end', '')
        d = self.kwargs.get('filter', '')
        query = Appointment.objects.all()
        today = datetime.today()

        if begin and end: # Preencheu o form
            try:
                begin = datetime.strptime(begin, '%d/%m/%Y')
                end = datetime.strptime(end, '%d/%m/%Y')
                # query = query.filter(day__gte=begin, day__lte=end)
            except:
                messages.error(self.request, 'Intervalo de datas inválido. Exibindo tudo!')
        elif d: # dropdown = tudo, hoje, mês, ano
            if d == 'tudo':
                return query
            elif d == 'hoje':
                begin = end = today
            elif d == 'essa-semana':
                begin = today - timedelta(days=today.isoweekday())
                end = begin + timedelta(days=6)
            elif d == 'esse-mes':
                begin = datetime(day=1, month=today.month, year=today.year)
                end = datetime(
                    day=calendar.monthrange(today.year, today.month)[1], month=today.month, year=today.year
                )
            elif d == 'esse-ano':
                begin = datetime(day=1, month=1, year=today.year)
                end = datetime(
                    day=calendar.monthrange(today.year, 12)[1], month=12, year=today.year
                )
        else: # Sem nada
            return query.filter(day__gte=today)

        self.request.GET.begin = begin.strftime('%d/%m/%Y')
        self.request.GET.end = end.strftime('%d/%m/%Y')
        query = query.filter(day__gte=begin, day__lte=end)
        return query

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['secretary'] = True
        return context

class ListDiariesViewInstructor(HasPermissionsMixin, ListView):
    required_permission = 'instructor'
    model = Appointment
    template_name = 'diary/list_appointments_instructor.html'
    context_object_name = 'appointments'
    paginate_by = 10

    def get_queryset(self):
        begin, end = self.request.GET.get('begin', ''), self.request.GET.get('end', '')
        d = self.kwargs.get('filter', '')
        query = Appointment.objects.filter(instructor__pk=self.request.user.pk)
        today = datetime.today()

        if begin and end: # Preencheu o form
            try:
                begin = datetime.strptime(begin, '%d/%m/%Y')
                end = datetime.strptime(end, '%d/%m/%Y')
                # query = query.filter(day__gte=begin, day__lte=end)
            except:
                messages.error(self.request, 'Intervalo de datas inválido. Exibindo tudo!')
        elif d: # dropdown = tudo, hoje, mês, ano
            if d == 'tudo':
                return query
            elif d == 'hoje':
                begin = end = today
            elif d == 'essa-semana':
                begin = today - timedelta(days=today.isoweekday())
                end = begin + timedelta(days=6)
            elif d == 'esse-mes':
                begin = datetime(day=1, month=today.month, year=today.year)
                end = datetime(
                    day=calendar.monthrange(today.year, today.month)[1], month=today.month, year=today.year
                )
            elif d == 'esse-ano':
                begin = datetime(day=1, month=1, year=today.year)
                end = datetime(
                    day=calendar.monthrange(today.year, 12)[1], month=12, year=today.year
                )
        else: # Sem nada
            return query.filter(day__gte=today)

        self.request.GET.begin = begin.strftime('%d/%m/%Y')
        self.request.GET.end = end.strftime('%d/%m/%Y')
        query = query.filter(day__gte=begin, day__lte=end)
        return query

class ListDiariesViewStudent(HasPermissionsMixin, ListView):
    required_permission = 'student'
    model = Appointment
    template_name = 'diary/list_appointments_student.html'
    context_object_name = 'appointments'
    paginate_by = 10

    def get_queryset(self):
        begin, end = self.request.GET.get('begin', ''), self.request.GET.get('end', '')
        d = self.kwargs.get('filter', '')
        query = Appointment.objects.filter(process__student__pk=self.request.user.pk)
        today = datetime.today()

        if begin and end: # Preencheu o form
            try:
                begin = datetime.strptime(begin, '%d/%m/%Y')
                end = datetime.strptime(end, '%d/%m/%Y')
                # query = query.filter(day__gte=begin, day__lte=end)
            except:
                messages.error(self.request, 'Intervalo de datas inválido. Exibindo tudo!')
        elif d: # dropdown = tudo, hoje, mês, ano
            if d == 'tudo':
                return query
            elif d == 'hoje':
                begin = end = today
            elif d == 'essa-semana':
                begin = today - timedelta(days=today.isoweekday())
                end = begin + timedelta(days=6)
            elif d == 'esse-mes':
                begin = datetime(day=1, month=today.month, year=today.year)
                end = datetime(
                    day=calendar.monthrange(today.year, today.month)[1], month=today.month, year=today.year
                )
            elif d == 'esse-ano':
                begin = datetime(day=1, month=1, year=today.year)
                end = datetime(
                    day=calendar.monthrange(today.year, 12)[1], month=12, year=today.year
                )
        else: # Sem nada
            return query.filter(day__gte=today)

        self.request.GET.begin = begin.strftime('%d/%m/%Y')
        self.request.GET.end = end.strftime('%d/%m/%Y')
        query = query.filter(day__gte=begin, day__lte=end)
        return query

class ListProcessDiariesView(ListView):
    model = Appointment
    template_name = 'diary/list_process_appointments.html'
    context_object_name = 'appointments'
    paginate_by = 10

    def get_queryset(self):
        return Appointment.objects.filter(process__pk=self.kwargs['pk_process'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['process'] = get_object_or_404(Process, pk=self.kwargs['pk_process'])
        return context

class RegisterAppointmentView(HasPermissionsMixin, SuccessMessageMixin, CreateView):
    required_permission = 'secretary'
    model = Appointment
    form_class = RegisterAppointmentForm
    template_name = 'diary/register_appointment.html'
    success_url = reverse_lazy('diary:list_diaries')
    success_message = 'Agendamento realizado com sucesso'

    def get_initial(self):
        initial = {}
        pk_process = self.kwargs.get('pk_process', '')
        if pk_process:
            process = get_object_or_404(Process, pk=pk_process)
            initial['process'] = process
        return initial

class RemoveAppointmentView(HasPermissionsMixin, DeleteView):
    required_permission = 'secretary'
    model = Appointment
    success_url = reverse_lazy('diary:list_diaries')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Agendamento removido com sucesso')
        return super().delete(request, *args, **kwargs)

class ConfirmAppointmentView(HasPermissionsMixin, SuccessMessageMixin, CreateView):
    required_permission = 'instructor'
    model = PracticalClass
    template_name = 'diary/confirm_appointment.html'
    success_url = reverse_lazy('diary:list_diaries')
    success_message = 'Aula registrada com sucesso'

    def get_initial(self):
        a = get_object_or_404(Appointment, pk=self.kwargs['pk'])
        return {
            'instructor': a.instructor,
            'simulator': a.simulator,
            'day': a.day,
            'begin_time': a.begin_time,
            'end_time': a.end_time
        }

    def get_form(self):
        return RegisterPracticalClassForm(**self.get_form_kwargs(), argumentos=self.kwargs)

    # Remover appointment
    def form_valid(self, form):
        app = get_object_or_404(Appointment, pk=self.kwargs['pk'])
        course = app.process.practical_course
        self.object = form.save(commit=False)
        self.object.practical_course = course
        self.object.save()
        return super().form_valid(form)

class DetailAppointmentView(HasPermissionsMixin, DetailView):
    required_permission = 'student'
    model = Appointment

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        person = Person.objects.get(pk=self.request.user.pk)
        context['person'] = person
        return context

list_diaries = ListDiariesView.as_view()
list_diaries_instructor = ListDiariesViewInstructor.as_view()
list_diaries_student = ListDiariesViewStudent.as_view()

list_diaries_process = ListProcessDiariesView.as_view()
detail_appointment = DetailAppointmentView.as_view()
register_appointment = RegisterAppointmentView.as_view()
remove_appointment = RemoveAppointmentView.as_view()
confirm_appointment = ConfirmAppointmentView.as_view()
