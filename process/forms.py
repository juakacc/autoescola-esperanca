from django import forms
from .models import Process, TheoreticalClass, PracticalClass
from accounts.models import Person
from core.validators import validar_carro, validar_end_time

class RegisterProcessForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Person.objects.filter(role_student=True)

    class Meta:
        model = Process
        fields = ['student', 'type_cnh', 'begin_date']

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

    def clean_vehicle(self):
        return validar_carro(self)

    def clean_end_time(self):
        return validar_end_time(self)

    class Meta:
        model = PracticalClass
        fields = ['instructor', 'simulator', 'vehicle', 'day', 'begin_time', 'end_time']

class RegisterPracticalClassFormInstructor(forms.ModelForm):
    process = forms.ModelChoiceField(queryset=Process.objects.all(), label='Processo')

    def clean_vehicle(self):
        return validar_carro(self)

    def clean_end_time(self):
        return validar_end_time(self)

    class Meta:
        model = PracticalClass
        fields = ['process', 'simulator', 'vehicle', 'day', 'begin_time', 'end_time']
