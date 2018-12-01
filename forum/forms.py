from django import forms
from .models import Reply

class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ['reply']
        labels = {
            'reply': 'Adicione uma resposta'
        }
        widgets = {
            'reply': forms.Textarea(attrs={'class':'form-control'})
        }
