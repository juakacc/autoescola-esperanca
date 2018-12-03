from django import forms
from news.models import New

class RegisterNewForm(forms.ModelForm):

    class Meta:
        model = New
        fields = ['title', 'slug', 'text', 'image']
        labels = {
            'title': 'Título *',
            'slug': 'Slug *',
            'text': 'Texto *',
            'image': 'Imagem'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            # 'image': forms.FileInput(attrs={'class': 'form-control'})
        }
