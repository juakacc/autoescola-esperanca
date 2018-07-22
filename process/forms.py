from django import forms
from .models import Process, TheoreticalClass, PracticalClass

class RegisterProcessForm(forms.ModelForm):

    class Meta:
        model = Process
        fields = ['student', 'type_cnh', 'date_start']

class RegisterTheoreticalClassForm(forms.ModelForm):

    class Meta:
        model = TheoreticalClass
        fields = ['instructor', 'day', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TextInput(attrs={'placeholder': 'HH:mm'}),
            'end_time': forms.TextInput(attrs={'placeholder': 'HH:mm'}),
        }

class RegisterPracticalClassForm(forms.ModelForm):

    def clean_vehicle(self):
        vehicle = self.cleaned_data['vehicle']
        simulator = self.cleaned_data['simulator']

        if simulator:
            vehicle = None
        else:
            if vehicle == None:
                raise forms.ValidationError('Escolha um veículo')
        return vehicle

    class Meta:
        model = PracticalClass
        fields = ['instructor', 'simulator', 'vehicle', 'day', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TextInput(attrs={'placeholder': 'HH:mm'}),
            'end_time': forms.TextInput(attrs={'placeholder': 'HH:mm'}),
        }
