from django import forms
from .models import Process

class RegisterProcessForm(forms.ModelForm):

    class Meta:
        model = Process
        fields = ['student', 'type_cnh', 'date_start']
