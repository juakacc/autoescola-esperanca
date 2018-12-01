from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import date

from core.models import Vehicle
from core.utils import generate_hash_key
from core.mail import send_mail_template
from .models import Person, PasswordReset

class RegisterEmployeeForm(UserCreationForm):
    password1 = forms.CharField(label='Senha *',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha com número e letras'}))
    password2 = forms.CharField(label='Confirmação de senha *',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita a senha'}))

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
        labels = {
            'cpf'          : 'CPF *',
            'username'     : 'Nome de usuário *',
            'name'         : 'Nome completo *',
            'date_of_birth': 'Data de nascimento *',
            'email'        : 'E-mail *',
            'telephone'    : 'Telefone *',
            'admission'    : 'Admitido em *',
            'role_admin'   : 'Administrador?',
            'role_secretary': 'Secretário?',
            'role_instructor': 'Instrutor?',
            'salary'       : 'Salário *',
            'cnh'          : 'CNH',
            'street'       : 'Rua *',
            'number'       : 'Número *',
            'district'     : 'Bairro *',
            'city'         : 'Cidade *',
            'state'        : 'Estado *'
        }
        widgets = {
            'cpf': forms.TextInput(attrs={'class':'form-control cpf', 'autofocus':True}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class':'form-control data'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'telephone': forms.TextInput(attrs={'class':'form-control telefone'}),
            'admission'    : forms.DateInput(attrs={'class':'form-control data'}),
            'role_admin'   : forms.Select(attrs={'class':'form-control'}),
            'role_secretary': forms.Select(attrs={'class':'form-control'}),
            'role_instructor': forms.Select(attrs={'class':'form-control'}),
            'salary'       : forms.NumberInput(attrs={'class':'form-control'}),
            'cnh': forms.NumberInput(attrs={'class':'form-control','placeholder': 'Caso seja um instrutor'}),
            'street': forms.TextInput(attrs={'class':'form-control'}),
            'number': forms.NumberInput(attrs={'class':'form-control'}),
            'district': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.Select(attrs={'class':'custom-select'}),
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

# Verificar se vai precisar
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']

        if Person.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError('Nenhum usuário cadastrado com esse e-mail')

    def save(self):
        user = Person.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.name)
        reset = PasswordReset(user=user, key=key)
        reset.save()
        template_name = 'accounts/password_reset_email.html'
        subject = 'Recuperação de senha - Autoescola Esperança'
        context = {
            'reset': reset
        }
        send_mail_template(subject, template_name, context, [user.email])

class RegisterStudentForm(UserCreationForm):
    password1 = forms.CharField(label='Senha *',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha com número e letras'}))
    password2 = forms.CharField(label='Confirmação de senha *',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita a senha'}))

    def clean_date_of_birth(self):
        born = self.cleaned_data['date_of_birth']
        if not is_date_of_birth_valid(born):
            raise forms.ValidationError('Um aluno não pode ser menor de idade')
        return born

    class Meta:
        model = Person
        fields = ['cpf', 'username', 'name', 'date_of_birth', 'email', 'telephone',
            'street', 'number', 'district', 'city', 'state']
        labels = {
            'cpf': 'CPF *',
            'username': 'Nome de usuário *',
            'name': 'Nome completo *',
            'date_of_birth': 'Data de nascimento *',
            'email': 'E-mail *',
            'telephone': 'Telefone *',
            'street': 'Rua *',
            'number': 'Número *',
            'district': 'Bairro *',
            'city': 'Cidade *',
            'state': 'Estado *'
        }
        widgets = {
            'cpf': forms.TextInput(attrs={'class':'form-control cpf', 'autofocus':True}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class':'form-control data'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'telephone': forms.TextInput(attrs={'class':'form-control telefone'}),
            'street': forms.TextInput(attrs={'class':'form-control'}),
            'number': forms.NumberInput(attrs={'class':'form-control'}),
            'district': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.Select(attrs={'class':'custom-select'}),
        }

def is_date_of_birth_valid(born):
    today = date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return age >= 18
