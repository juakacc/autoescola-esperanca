from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import date

from core.models import Vehicle
from .models import Employee, Student

class RegisterSecretaryForm(UserCreationForm):
    def clean_date_of_birth(self):
        born = self.cleaned_data['date_of_birth']
        if not is_date_of_birth_valid(born):
            raise forms.ValidationError('Um funcionário não pode ser menor de idade')
        return born

    class Meta:
        model = Employee
        fields = ['username', 'name', 'cpf', 'date_of_birth', 'email', 'telephone', 'salary',
            'street', 'number', 'district', 'city', 'state']

class RegisterStudentForm(UserCreationForm):

    def clean_date_of_birth(self):
        born = self.cleaned_data['date_of_birth']
        if not is_date_of_birth_valid(born):
            raise forms.ValidationError('Um aluno não pode ser menor de idade')
        return born

    class Meta:
        model = Student
        fields = ['username', 'name', 'cpf', 'date_of_birth', 'email', 'telephone',
            'street', 'number', 'district', 'city', 'state']

class RegisterInstructorForm(UserCreationForm):
    def clean_date_of_birth(self):
        born = self.cleaned_data['date_of_birth']
        if not is_date_of_birth_valid(born):
            raise forms.ValidationError('Um funcionário não pode ser menor de idade')
        return born
        # tem q ser maior q 21

    class Meta:
        model = Employee
        fields = ['username', 'name', 'cpf', 'date_of_birth', 'email', 'telephone', 'salary', 'cnh',
            'street', 'number', 'district', 'city', 'state']

def is_date_of_birth_valid(born):
    today = date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return age >= 18
