from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import date

from core.models import Vehicle
from core.utils import generate_hash_key
from core.mail import send_mail_template
from .models import Person, PasswordReset

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
