from django.db import models
from datetime import datetime, date
from accounts.models import Student, Employee
from core.models import Vehicle

STATUS_CHOICES = (
    ('nao iniciado', 'Não iniciado'),
    ('iniciado', 'Iniciado'),
    ('concluido', 'Concluído'),
)

class Exam(models.Model):
    exam_medical = models.BooleanField('Exame médico', default=False)
    exam_psychological = models.BooleanField('Exame psicológico', default=False)
    date_exam = models.DateField('Data do exame', null=True, default=None)

    status = models.CharField('Status', max_length=20, default='Iniciado', choices=STATUS_CHOICES)

    def __str__(self):
        return 'Exames de ' + self.process.student.__str__()

class TheoreticalCourse(models.Model):
    status = models.CharField('Status', max_length=20, default='Não iniciado', choices=STATUS_CHOICES)

    def count_classes(self):
        return len(self.aulas.all())

    class Meta:
        verbose_name = 'Curso teórico'
        verbose_name_plural = 'Cursos teóricos'

    def __str__(self):
        return 'Curso teórico de ' + self.process.student.__str__()

class PracticalCourse(models.Model):
    vehicle = models.ForeignKey(Vehicle, verbose_name='Veículo', on_delete=models.SET_NULL, null=True, default=None)
    status = models.CharField('Status', max_length=20, default='Não iniciado', choices=STATUS_CHOICES)

    def count_classes_car(self):
        return len(self.aulas.filter(simulator=False))

    def count_classes_simulator(self):
        return len(self.aulas.filter(simulator=True))

    class Meta:
        verbose_name = 'Curso prático'
        verbose_name_plural = 'Cursos práticos'

    def __str__(self):
        return 'Curso prático de ' + self.process.student.__str__()

class Process(models.Model):

    student = models.ForeignKey(Student, verbose_name='Aluno', on_delete=models.CASCADE)
    type_cnh = models.CharField('Tipo da CNH', choices=Employee.TYPE_CHOICES, max_length=3)

    date_start = models.DateField('Início', default=datetime.now)
    date_end = models.DateField('Fim', blank=True, null=True, default=None)
    status = models.CharField('Status', max_length=20, default='Iniciado', choices=STATUS_CHOICES)

    exams = models.OneToOneField(Exam, verbose_name='Exames', on_delete=models.CASCADE, blank=True, default=None, null=True)
    theoretical_course = models.OneToOneField(TheoreticalCourse, verbose_name='Curso teórico', on_delete=models.CASCADE, blank=True, default=None, null=True)
    practical_course = models.OneToOneField(PracticalCourse, verbose_name='Curso prático', on_delete=models.CASCADE, blank=True, default=None, null=True)

    def get_percent(self):
        return 50

    def __str__(self):
        return 'Proc. de ' + self.student.__str__()

    class Meta:
        verbose_name = 'Processo'
        verbose_name_plural = 'Processos'
        ordering = ['-date_start']

class TheoreticalClass(models.Model):
    theoretical_course = models.ForeignKey(TheoreticalCourse, related_name='aulas', verbose_name='Curso teórico', on_delete=models.CASCADE)
    instructor = models.ForeignKey(Employee, verbose_name='Instrutor', on_delete=models.SET_NULL, null=True)
    day = models.DateField('Dia da aula')
    start_time = models.DateTimeField('Hora do início')
    end_time = models.DateTimeField('Hora do fim')

    class Meta:
        verbose_name = 'Aula teórica'
        verbose_name_plural = 'Aulas teóricas'

class PracticalClass(models.Model):
    practical_course = models.ForeignKey(PracticalCourse, related_name='aulas', verbose_name='Curso prático', on_delete=models.CASCADE)
    instructor = models.ForeignKey(Employee, verbose_name='Instrutor', on_delete=models.SET_NULL, null=True)
    simulator = models.BooleanField('Aula de simulador', default=False)
    # vehicle = models.ForeignKey(Vehicle, verbose_name='Veículo', on_delete=models.SET_NULL, null=True, default=None)
    day = models.DateField('Dia da aula')
    start_time = models.DateTimeField('Hora do início')
    end_time = models.DateTimeField('Hora do fim')

    class Meta:
        verbose_name = 'Aula prática'
        verbose_name_plural = 'Aulas práticas'

def create_process(instance, created, **kwargs):
    if created:
        instance.exams = Exam.objects.create()
        instance.theoretical_course = TheoreticalCourse.objects.create()
        instance.practical_course = PracticalCourse.objects.create()
        instance.save()

def update_end_date(instance, **kwargs):
    # Atualizando a data final do processo: 1 ano
    instance.date_end = date.fromordinal(instance.date_start.toordinal()+365)

models.signals.post_save.connect(
    create_process, sender=Process, dispatch_uid='create_process'
)
models.signals.pre_save.connect(
    update_end_date, sender=Process, dispatch_uid='update_end_date'
)
