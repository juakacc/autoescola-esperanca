from django import forms
from .models import Contact

class ResponseContactForm(forms.ModelForm):
# Formulário para responder um contato
    class Meta:
        model = Contact
        fields = ['response']

    def send_email(self, obj):
        print('E-mail enviado com sucesso: ' + obj.response + ' de: ' + obj.subject)
        pass
