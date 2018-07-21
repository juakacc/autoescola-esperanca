from django import forms
from .models import Process, TheoreticalClass

class RegisterProcessForm(forms.ModelForm):

    class Meta:
        model = Process
        fields = ['student', 'type_cnh', 'date_start']

class RegisterClassForm(forms.ModelForm):

    class Meta:
        model = TheoreticalClass
        fields = ['instructor', 'day', 'start_time', 'end_time']
