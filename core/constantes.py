from datetime import time

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

# estado do veículo
FUNCIONANDO = 'Funcionando'
EM_CONSERTO = 'Em conserto'
