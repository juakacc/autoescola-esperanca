from django import forms
from .models import Contact, Vehicle

class ResponseContactForm(forms.ModelForm):
    ''' Formulário para responder um contato '''
    class Meta:
        model = Contact
        fields = ['response']

    def send_email(self, obj):
        print('E-mail enviado com sucesso: ' + obj.response + ' de: ' + obj.subject)

class RegisterVehicleForm(forms.ModelForm):
    ''' Formulário para registrar um veículo '''
    class Meta:
        model = Vehicle
        fields = ['type', 'slug', 'fabricator', 'model', 'year', 'plate']
        widgets = {
            'slug': forms.TextInput(attrs={'placeholder': 'carro-01, moto-01...'}),
            'plate': forms.TextInput(attrs={'placeholder': 'AAA-1111'})
        }
