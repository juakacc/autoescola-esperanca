from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy

from datetime import datetime, timedelta
import calendar

from process.forms import RegisterPracticalClassForm
from process.models import PracticalClass
from .forms import RegisterAppointmentForm
from .models import Appointment

class ListDiariesView(ListView):
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

class RegisterAppointmentView(SuccessMessageMixin, CreateView):
    model = Appointment
    form_class = RegisterAppointmentForm
    template_name = 'diary/register_appointment.html'
    success_url = reverse_lazy('diary:list_diaries')
    success_message = 'Agendamento realizado com sucesso'

class RemoveAppointmentView(DeleteView):
    model = Appointment
    success_url = reverse_lazy('diary:list_diaries')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Agendamento removido com sucesso')
        return super().delete(request, *args, **kwargs)

class ConfirmAppointmentView(SuccessMessageMixin, CreateView):
    model = PracticalClass
    form_class = RegisterPracticalClassForm
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

    def form_valid(self, form):
        app = get_object_or_404(Appointment, pk=self.kwargs['pk'])
        course = app.process.practical_course
        self.object = form.save(commit=False)
        self.object.practical_course = course
        self.object.save()
        return super().form_valid(form)

class DetailAppointmentView(DetailView):
    model = Appointment

list_diaries = ListDiariesView.as_view()
detail_appointment = DetailAppointmentView.as_view()
register_appointment = RegisterAppointmentView.as_view()
remove_appointment = RemoveAppointmentView.as_view()
confirm_appointment = ConfirmAppointmentView.as_view()
