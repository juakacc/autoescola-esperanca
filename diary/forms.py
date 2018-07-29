from django import forms
from .models import Appointment
from process.models import Process
from accounts.models import Person
from core.constantes import *

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
        fields = '__all__'
