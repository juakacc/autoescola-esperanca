from django import forms
from .models import Message

class RegisterMessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['to', 'subject', 'message']
