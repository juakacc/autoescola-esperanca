from django import forms
from .models import Process, TheoreticalClass, PracticalClass
from accounts.models import Person

from core.constantes import *
from core.models import Vehicle
from core.validators import validar_carro, validar_end_time

class RegisterProcessForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Person.objects.filter(role_student=True, process__isnull=True)

    class Meta:
        model = Process
        fields = ['student', 'type_cnh', 'begin_date']
        labels = {
            'student': 'Aluno *',
            'type_cnh': 'Tipo da CNH *',
            'begin_date': 'Data de Início *'
        }
        widgets = {
            'student': forms.Select(attrs={'class':'custom-select'}),
            'type_cnh': forms.Select(attrs={'class':'custom-select'}),
            'begin_date': forms.DateInput(attrs={'class':'form-control data'})
        }

class RegisterTheoreticalClassForm(forms.ModelForm):
    ''' Para registro de aula teórica pelo secretário '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instructor'].queryset = Person.objects.filter(role_instructor=True)

    def clean_end_time(self):
        return validar_end_time(self)

    class Meta:
        model = TheoreticalClass
        fields = ['instructor', 'day', 'begin_time', 'end_time']

class RegisterTheoreticalClassFormInstructor(forms.ModelForm):
    process = forms.ModelChoiceField(label='Processo', queryset=Process.objects.all())

    def clean_end_time(self):
        return validar_end_time(self)

    class Meta:
        model = TheoreticalClass
        fields = ['process', 'day', 'begin_time', 'end_time']

class RegisterPracticalClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instructor'].queryset = Person.objects.filter(role_instructor=True)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(state=FUNCIONANDO)

    def clean_vehicle(self):
        return validar_carro(self)

    def clean_end_time(self):
        return validar_end_time(self)

    class Meta:
        model = PracticalClass
        fields = ['instructor', 'simulator', 'vehicle', 'day', 'begin_time', 'end_time']

class RegisterPracticalClassFormInstructor(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(state=FUNCIONANDO)

    process = forms.ModelChoiceField(queryset=Process.objects.all(), label='Processo')

    def clean_vehicle(self):
        return validar_carro(self)

    def clean_end_time(self):
        return validar_end_time(self)

    class Meta:
        model = PracticalClass
        fields = ['process', 'simulator', 'vehicle', 'day', 'begin_time', 'end_time']
