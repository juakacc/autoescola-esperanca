from datetime import time

# Para seleção de horários
HORARY = (
    (time(7, 0), '07:00'),
    (time(7, 30), '07:30'),
    (time(8, 0), '08:00'),
    (time(8, 30), '08:30'),
    (time(9, 0), '09:00'),
    (time(9, 30), '09:30'),
    (time(10, 0), '10:00'),
    (time(10, 30), '10:30'),
    (time(11, 0), '11:00'),
    (time(11, 30), '11:30'),
    (time(12, 0), '12:00'),
    (time(12, 30), '12:30'),
    (time(13, 0), '13:00'),
    (time(13, 30), '13:30'),
    (time(14, 0), '14:00'),
    (time(14, 30), '14:30'),
    (time(15, 0), '15:00'),
    (time(15, 30), '15:30'),
    (time(16, 0), '16:00'),
    (time(16, 30), '16:30'),
    (time(17, 0), '17:00'),
    (time(17, 30), '17:30'),
    (time(18, 0), '18:00'),
    (time(18, 30), '18:30'),
    (time(19, 0), '19:00'),
    (time(19, 30), '19:30'),
    (time(20, 0), '20:00'),
)

# status dos processos
NAO_INICIADO = 'nao_iniciado'
INICIADO = 'iniciado'
CONCLUIDO = 'concluido'
VENCIDO = 'vencido'

# estado do veículo
FUNCIONANDO = 'Funcionando'
EM_CONSERTO = 'Em conserto'

# Estados para seleção
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

# Tipos de usuários
ADMIN = 'admin'
SECRETARY = 'secretario'
INSTRUCTOR = 'instrutor'
STUDENT = 'aluno'

FUNCTION_CHOICES = (
    (ADMIN, 'Admin'),
    (SECRETARY, 'Secretário'),
    (INSTRUCTOR, 'Instrutor'),
    (STUDENT, 'Aluno')
)

# Tipos de habilitação
ACC = 'ACC'
A = 'A'
B = 'B'
AB = 'AB'
C = 'C'
AC = 'AC'
D = 'D'
AD = 'AD'
E = 'E'
AE = 'AE'

TYPE_CNH_CHOICES = (
    (ACC, 'ACC'),
    (A, 'A'),
    (B, 'B'),
    (AB, 'A/B'),
    (C, 'C'),
    (AC, 'A/C'),
    (D, 'D'),
    (AD, 'A/D'),
    (E, 'E'),
    (AE, 'A/E'),
)
# Status de processo
COURSE_STATUS = (
    (NAO_INICIADO, 'Não iniciado'),
    (INICIADO, 'Iniciado'),
    (CONCLUIDO, 'Concluído'),
)
