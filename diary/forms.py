from django import forms
from .models import Appointment
from process.models import Process, PracticalCourse, PracticalClass
from accounts.models import Person

from core.models import Vehicle
from core.constantes import *
from core.validators import validar_carro, validar_end_time


class RegisterAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instructor'].queryset = Person.objects.filter(role_instructor=True)
        self.fields['process'].queryset = Process.objects.filter(theoretical_course__status=CONCLUIDO)

    def clean_process(self):
        process = self.cleaned_data['process']
        if process.theoretical_course.status != CONCLUIDO:
            raise forms.ValidationError('Curso teórico ainda não concluído')
        return process

    def clean_end_time(self):
        begin = self.cleaned_data['begin_time']
        end = self.cleaned_data['end_time']
        if begin > end:
            raise forms.ValidationError('Tempo final não pode ser menor que o tempo inicial')
        return end

    class Meta:
        model = Appointment
        fields = ['instructor', 'process', 'simulator', 'day', 'begin_time', 'end_time']
        labels = {
            'instructor': 'Instrutor *',
            'process': 'Processo *',
            'simulator': 'Aula no simulador?',
            'day': 'Data *',
            'begin_time': 'Horário inicial *',
            'end_time': 'Horário final *'
        }
        widgets = {
            'instructor': forms.Select(attrs={'class':'custom-select'}),
            'process': forms.Select(attrs={'class':'custom-select'}),
            'simulator': forms.Select(attrs={'class':'custom-select'}),
            'day': forms.DateInput(attrs={'class':'form-control'}),
            'begin_time': forms.Select(attrs={'class':'custom-select'}),
            'end_time': forms.Select(attrs={'class':'custom-select'})
        }

class RegisterPracticalClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.argumentos = kwargs.pop('argumentos', None)
        super().__init__(*args, **kwargs)
        self.fields['instructor'].queryset = Person.objects.filter(role_instructor=True)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(state=FUNCIONANDO)

    def clean_vehicle(self):
        return validar_carro(self)

    def clean_end_time(self):
        return validar_end_time(self)

    def clean_day(self):
        day = self.cleaned_data['day']
        ap = Appointment.objects.get(pk=self.argumentos['pk'])

        begin_day_process = Process.objects.get(pk=ap.process.pk).begin_date

        if (begin_day_process > day):
            raise forms.ValidationError('Essa data é anterior ao início do processo : {}'.format(
                begin_day_process
            ))
        return day

    class Meta:
        model = PracticalClass
        fields = ['instructor', 'simulator', 'vehicle', 'day', 'begin_time', 'end_time']
        labels = {
            'instructor':'Instrutor *',
            'simulator':'Aula de simulador? *',
            'vehicle':'Veículo (obrigatório para aula veicular)',
            'day':'Data *',
            'begin_time':'Horário inicial *',
            'end_time':'Horário final *'
        }
        widgets = {
            'instructor':forms.Select(attrs={'class':'custom-select'}),
            'simulator':forms.Select(attrs={'class':'custom-select'}),
            'vehicle':forms.Select(attrs={'class':'custom-select'}),
            'day': forms.DateInput(attrs={'class':'form-control data'}),
            'begin_time':forms.Select(attrs={'class':'custom-select'}),
            'end_time':forms.Select(attrs={'class':'custom-select'}),
        }
