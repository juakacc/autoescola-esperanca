from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from core.models import Employee, Student
from .models import Vehicle

class RegisterSecretaryForm(UserCreationForm):

    class Meta:
        model = Employee
        fields = ['username', 'name', 'cpf', 'date_of_birth', 'email', 'telephone', 'salary',
            'street', 'number', 'district', 'city', 'state']

class RegisterStudentForm(UserCreationForm):

    class Meta:
        model = Student
        fields = ['username', 'name', 'cpf', 'date_of_birth', 'email', 'telephone',
            'street', 'number', 'district', 'city', 'state']

class RegisterInstructorForm(UserCreationForm):

    class Meta:
        model = Employee
        fields = ['username', 'name', 'cpf', 'date_of_birth', 'email', 'telephone', 'salary', 'cnh', 'type_cnh',
            'street', 'number', 'district', 'city', 'state']
