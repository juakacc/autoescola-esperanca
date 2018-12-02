from django import forms
from .models import Process, TheoreticalClass, PracticalClass, Exam
from accounts.models import Person

from core.constantes import *
from core.models import Vehicle
from core.validators import validar_carro, validar_end_time, validar_day

class UpdateExamsForm(forms.ModelForm):
    ''' Formulário para atualização de exames do processo '''
    class Meta:
        model = Exam
        fields = ['exam_medical', 'exam_psychological']
        labels = {
            'exam_medical': 'Exame médico *',
            'exam_psychological': 'Exame psicológico'
        }
        widgets = {
            'exam_medical': forms.Select(attrs={'class':'custom-select'}),
            'exam_psychological': forms.Select(attrs={'class':'custom-select'}),
        }

class RegisterProcessForm(forms.ModelForm):
    ''' Formulário para registro de um novo processo '''
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

class UpdateProcessForm(forms.ModelForm):

    class Meta:
        model = Process
        fields = ['type_cnh', 'begin_date']
        labels = {
            'type_cnh': 'Tipo da CNH *',
            'begin_date': 'Data de início *'
        }
        widgets = {
            'type_cnh': forms.Select(attrs={'class':'custom-select'}),
            'begin_date': forms.DateInput(attrs={'class':'form-control data'})
        }

class RegisterTheoreticalClassForm(forms.ModelForm):
    ''' Para registro de aula teórica pelo secretário '''
    def __init__(self, *args, **kwargs):
        self.argumentos = kwargs.pop('argumentos', None)
        super().__init__(*args, **kwargs)
        self.fields['instructor'].queryset = Person.objects.filter(role_instructor=True)

    def clean_end_time(self):
        return validar_end_time(self)

    def clean_day(self):
        return validar_day(self)

    class Meta:
        model = TheoreticalClass
        fields = ['instructor', 'day', 'begin_time', 'end_time']
        labels = {
            'instructor': 'Instrutor *',
            'day': 'Data *',
            'begin_time': 'Horário incial *',
            'end_time': 'Horário final *'
        }
        widgets = {
            'instructor': forms.Select(attrs={'class':'custom-select'}),
            'day': forms.DateInput(attrs={'class':'form-control data'}),
            'begin_time': forms.Select(attrs={'class':'custom-select'}),
            'end_time': forms.Select(attrs={'class':'custom-select'}),
        }

class RegisterTheoreticalClassFormInstructor(forms.ModelForm):
    ''' Para registro de aula teórica pelo instrutor '''
    def __init__(self, *args, **kwargs):
        self.argumentos = kwargs.pop('argumentos', None)
        super().__init__(*args, **kwargs)

    process = forms.ModelChoiceField(label='Processo', queryset=Process.objects.all())

    def clean_end_time(self):
        return validar_end_time(self)

    def clean_day(self):
        return validar_day(self)

    class Meta:
        model = TheoreticalClass
        fields = ['process', 'day', 'begin_time', 'end_time']
        labels = {
            'instructor': 'Instrutor *',
            'day': 'Data *',
            'begin_time': 'Horário incial *',
            'end_time': 'Horário final *'
        }
        widgets = {
            'instructor': forms.Select(attrs={'class':'custom-select'}),
            'day': forms.DateInput(attrs={'class':'form-control data'}),
            'begin_time': forms.Select(attrs={'class':'custom-select'}),
            'end_time': forms.Select(attrs={'class':'custom-select'}),
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
        return validar_day(self)

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

class RegisterPracticalClassFormInstructor(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.argumentos = kwargs.pop('argumentos', None)
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(state=FUNCIONANDO)

    process = forms.ModelChoiceField(queryset=Process.objects.all(), label='Processo')

    def clean_vehicle(self):
        return validar_carro(self)

    def clean_end_time(self):
        return validar_end_time(self)

    def clean_day(self):
        return validar_day(self)

    class Meta:
        model = PracticalClass
        fields = ['process', 'simulator', 'vehicle', 'day', 'begin_time', 'end_time']
        labels = {
            'process':'Processo *',
            'simulator':'Aula de simulador? *',
            'vehicle':'Veículo (obrigatório para aula veicular)',
            'day':'Data *',
            'begin_time':'Horário inicial *',
            'end_time':'Horário final *'
        }
        widgets = {
            'process':forms.Select(attrs={'class':'custom-select'}),
            'simulator':forms.Select(attrs={'class':'custom-select'}),
            'vehicle':forms.Select(attrs={'class':'custom-select'}),
            'day': forms.DateInput(attrs={'class':'form-control data'}),
            'begin_time':forms.Select(attrs={'class':'custom-select'}),
            'end_time':forms.Select(attrs={'class':'custom-select'}),
        }
