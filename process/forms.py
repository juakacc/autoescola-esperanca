from django import forms
from .models import Process, TheoreticalClass, PracticalClass
from accounts.models import Employee

class RegisterProcessForm(forms.ModelForm):

    class Meta:
        model = Process
        fields = ['student', 'type_cnh', 'begin_date']

class RegisterTheoreticalClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instructor'].queryset = Employee.objects.filter(function='instrutor')

    def clean_end_time(self):
        begin = self.cleaned_data['begin_time']
        end = self.cleaned_data['end_time']
        if begin > end:
            raise forms.ValidationError('Tempo final não pode ser menor que o tempo inicial')
        return end

    class Meta:
        model = TheoreticalClass
        fields = ['instructor', 'day', 'begin_time', 'end_time']
        # widgets = {
        #     # 'begin_time': forms.TextInput(attrs={'placeholder': 'HH:mm'}),
        #     # 'end_time': forms.TextInput(attrs={'placeholder': 'HH:mm'}),
        # }

class RegisterPracticalClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instructor'].queryset = Employee.objects.filter(function='instrutor')

    def clean_vehicle(self):
        vehicle = self.cleaned_data['vehicle']
        simulator = self.cleaned_data['simulator']

        if simulator:
            return None
        else:
            if not vehicle:
                raise forms.ValidationError('Escolha um veículo')
            return vehicle

    def clean_end_time(self):
        begin = self.cleaned_data['begin_time']
        end = self.cleaned_data['end_time']
        if begin > end:
            raise forms.ValidationError('Tempo final não pode ser menor que o tempo inicial')
        return end

    class Meta:
        model = PracticalClass
        fields = ['instructor', 'simulator', 'vehicle', 'day', 'begin_time', 'end_time']
        # widgets = {
        #     'begin_time': forms.TextInput(attrs={'placeholder': 'HH:mm'}),
        #     'end_time': forms.TextInput(attrs={'placeholder': 'HH:mm'}),
        # }
