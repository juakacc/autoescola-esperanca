from django import forms
from .models import Message

class RegisterMessageForm(forms.ModelForm):
    ''' Formulário para registrar uma mensagem para uma determinada pessoa '''
    class Meta:
        model = Message
        fields = ['to', 'subject', 'message']

class RegisterResponseForm(forms.ModelForm):
    ''' Formulário para registrar a reposta para uma mensagem '''
    class Meta:
        model = Message
        fields = ['message']
