from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import date

from core.models import Vehicle
from .models import Person

class RegisterEmployeeForm(UserCreationForm):
    def clean_date_of_birth(self):
        born = self.cleaned_data['date_of_birth']
        if not is_date_of_birth_valid(born):
            raise forms.ValidationError('Um funcionário não pode ser menor de idade')
        return born

    def clean_cnh(self):
        cnh = self.cleaned_data['cnh']
        instructor = self.cleaned_data['role_instructor']

        if instructor:
            if not cnh:
                raise forms.ValidationError('O número da CNH é obrigatório para um instrutor')
        return cnh

    class Meta:
        model = Person
        fields = ['cpf', 'username', 'name', 'date_of_birth', 'email', 'telephone', 'admission',
            'role_admin', 'role_secretary', 'role_instructor', 'salary', 'cnh', 'street', 'number',
            'district', 'city', 'state']
        widgets = {
            'cnh': forms.TextInput(attrs={'placeholder': 'Caso seja um instrutor'})
        }

class UpdateEmployeeForm(forms.ModelForm):
    def clean_date_of_birth(self):
        born = self.cleaned_data['date_of_birth']
        if not is_date_of_birth_valid(born):
            raise forms.ValidationError('Um funcionário não pode ser menor de idade')
        return born

    def clean_cnh(self):
        cnh = self.cleaned_data['cnh']
        instructor = self.cleaned_data['role_instructor']

        if instructor:
            if not cnh:
                raise forms.ValidationError('O número da CNH é obrigatório para um instrutor')
        return cnh
    class Meta:
        model = Person
        fields = ['cpf', 'username', 'name', 'date_of_birth', 'email', 'telephone', 'admission',
            'role_secretary', 'role_instructor', 'salary', 'cnh', 'street', 'number',
            'district', 'city', 'state']

class RegisterStudentForm(UserCreationForm):

    def clean_date_of_birth(self):
        born = self.cleaned_data['date_of_birth']
        if not is_date_of_birth_valid(born):
            raise forms.ValidationError('Um aluno não pode ser menor de idade')
        return born

    class Meta:
        model = Person
        fields = ['cpf', 'username', 'name', 'date_of_birth', 'email', 'telephone',
            'street', 'number', 'district', 'city', 'state']

def is_date_of_birth_valid(born):
    today = date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return age >= 18
