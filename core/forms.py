from django import forms
from .models import Contact, Vehicle
from core.models import SystemSettings

class ResponseContactForm(forms.ModelForm):
    ''' Formulário para responder um contato '''
    class Meta:
        model = Contact
        fields = ['response']

    def send_email(self, obj):
        print('E-mail enviado com sucesso: ' + obj.response + ' de: ' + obj.subject)

class UpdateSettingsForm(forms.ModelForm):
    ''' Formulário para atualizar as configurações gerais '''
    class Meta:
        model = SystemSettings
        fields = ['basic_salary', 'hours_theoretical', 'hours_practical_simulator', 'hours_practical_vehicle', 'begin_expedient', 'end_expedient']
        labels = {
            'basic_salary': 'Salário básico *',
            'hours_theoretical': 'Quantidade de horas teóricas *',
            'hours_practical_simulator': 'Quantidade de horas no simulador *',
            'hours_practical_vehicle': 'Quantidade de horas práticas *',
            'begin_expedient': 'Horário do início do expediente *',
            'end_expedient': 'Horário do fim do expediente *'
        }
        widgets = {
            'basic_salary': forms.NumberInput(attrs={'class':'form-control'}),
            'hours_theoretical': forms.NumberInput(attrs={'class':'form-control'}),
            'hours_practical_simulator': forms.NumberInput(attrs={'class':'form-control'}),
            'hours_practical_vehicle': forms.NumberInput(attrs={'class':'form-control'}),
            'begin_expedient': forms.Select(attrs={'class': 'custom-select'}),
            'end_expedient': forms.Select(attrs={'class': 'custom-select'})
        }

class RegisterVehicleForm(forms.ModelForm):
    ''' Formulário para registrar um veículo '''
    class Meta:
        model = Vehicle
        fields = ['type', 'slug', 'fabricator', 'model', 'year', 'plate']
        labels = {
            'type': 'Tipo *',
            'slug': 'Apelido *',
            'fabricator': 'Fabricante *',
            'model': 'Modelo *',
            'year': 'Ano *',
            'plate': 'Placa *'
        }

        widgets = {
            'type': forms.Select(attrs={'class': 'custom-select'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'carro-01, moto-01...'}),
            'fabricator': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'plate': forms.TextInput(attrs={'class': 'form-control placa_veiculo', 'placeholder': 'AAA-1111'})
        }

class ContactForm(forms.ModelForm):
    ''' Formulário para contato com a autoescola '''
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        labels = {
            'name': 'Nome *',
            'email': 'E-mail *',
            'subject': 'Assunto *',
            'message': 'Mensagem *'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'})
        }
