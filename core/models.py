from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
    class Meta:
        verbose_name = 'Usuário'

class Person(User):
    name = models.CharField('Nome', max_length=100)
    cpf = models.CharField('CPF', max_length=11, unique=True)
    date_of_birth = models.DateField('Data de nascimento')
    telephone = models.CharField('Telefone', max_length=20)

    STATES_CHOICE = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    )
    street = models.CharField('Rua', max_length=200)
    number = models.PositiveIntegerField('Número')
    district = models.CharField('Bairro', max_length=100)
    city = models.CharField('Cidade', max_length=100)
    state = models.CharField('Estado', max_length=2,
        choices=STATES_CHOICE, default='PB')

    created = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Pessoa'

class Employee(Person):
    FUNCTION_CHOICES = (
        ('secretario', 'Secretário'),
        ('instrutor', 'Instrutor')
    )
    function = models.CharField('Função', max_length=20, choices=FUNCTION_CHOICES)
    salary = models.DecimalField(verbose_name='Salário', max_digits=8, decimal_places=2)
    registry = models.CharField('Matrícula', max_length=10)

    TYPE_CHOICES = (
        ('ACC', 'ACC'),
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'A/B'),
        ('C', 'C'),
        ('AC', 'A/C'),
        ('D', 'D'),
        ('AD', 'A/D'),
        ('E', 'E'),
        ('AE', 'A/E'),
    )
    cnh = models.CharField('CNH', max_length=20, null=True)
    type_cnh = models.CharField('Tipo da CNH', max_length=3, choices=TYPE_CHOICES, null=True, default='AB')

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

class Student(Person):
    pass
    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

# Para contato de visitante com o administrador
class Contact(models.Model):
    name = models.CharField('Nome', max_length=100)
    email = models.EmailField('E-mail')
    subject = models.CharField('Assunto', max_length=100)
    message = models.TextField('Mensagem')
    visualized = models.BooleanField('Vista', default=False)

    created = models.DateTimeField('Data', auto_now_add=True)

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
        ordering = ['-created']

# class SiteSettings(models.Model):
#     basic_salary = models.DecimalField('Salário Mínimo', max_digits=8, decimal_places=2)
