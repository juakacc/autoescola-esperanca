from django import forms
from news.models import New

class RegisterNewForm(forms.ModelForm):

    class Meta:
        model = New
        fields = ['title', 'slug', 'text', 'image']
