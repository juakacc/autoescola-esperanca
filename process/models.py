from django.shortcuts import reverse
from django.db import models
from datetime import datetime, date
from accounts.models import Student, Employee
from core.models import Vehicle, SystemSettings

NAO_INICIADO = 'nao_iniciado'
INICIADO = 'iniciado'
CONCLUIDO = 'concluido'

STATUS_CHOICES = (
    (NAO_INICIADO, 'Não iniciado'),
    (INICIADO, 'Iniciado'),
    (CONCLUIDO, 'Concluído'),
)

class Exam(models.Model):
    APTO_CHOICES = (
        (True, 'Apto'),
        (False, 'Não apto')
    )

    exam_medical = models.BooleanField('Exame médico', default=False, choices=APTO_CHOICES)
    exam_psychological = models.BooleanField('Exame psicológico', default=False, choices=APTO_CHOICES)
    date_exam = models.DateField('Data do exame', null=True, default=None)

    status = models.CharField('Status', max_length=20, default=INICIADO, choices=STATUS_CHOICES)

    def get_percent(self):
        if self.status == CONCLUIDO:
            return 100
        elif self.exam_medical or self.exam_psychological:
            return 50
        else:
            return 0

    def __str__(self):
        return 'Exames de ' + self.process.student.__str__()

class TheoreticalCourse(models.Model):
    status = models.CharField('Status', max_length=20, default=NAO_INICIADO, choices=STATUS_CHOICES)

    def count_classes(self):
        '''Retorna a quantidate de horas já concluídas'''
        aulas, horas = self.aulas.all(), 0

        for aula in aulas:
            hora_aula = datetime.combine(date.min, aula.end_time) - datetime.combine(date.min, aula.begin_time)
            horas += (hora_aula.seconds / 3600)
        return horas

    def get_percent(self):
        ''' Percentual do curso teórico concluído '''
        total_hours = SystemSettings.objects.all()[0].hours_theoretical
        return self.count_classes() / total_hours * 100

    def get_absolute_url(self):
        return reverse('process:theoretical_course', kwargs={'pk_process': self.process.pk})

    class Meta:
        verbose_name = 'Curso teórico'
        verbose_name_plural = 'Cursos teóricos'

    def __str__(self):
        return 'Curso teórico de ' + self.process.student.__str__()

class PracticalCourse(models.Model):
    status = models.CharField('Status', max_length=20, default=NAO_INICIADO, choices=STATUS_CHOICES)

    total_hours = models.PositiveIntegerField('Horas práticas necessárias', default=20)

    def count_classes_car(self):
        ''' Calcula o total de horas realizadas no veículo '''
        aulas, horas = self.aulas.filter(simulator=False), 0
        for aula in aulas:
            hora_aula = datetime.combine(date.min, aula.end_time) - datetime.combine(date.min, aula.begin_time)
            horas += (hora_aula.seconds / 3600)
        return horas

    def count_classes_simulator(self):
        ''' Calcula o total de horas realizadas no simulador '''
        aulas, horas = self.aulas.filter(simulator=True), 0
        for aula in aulas:
            hora_aula = datetime.combine(date.min, aula.end_time) - datetime.combine(date.min, aula.begin_time)
            horas += (hora_aula.seconds / 3600)
        return horas

    def get_percent(self):
        ''' Percentual de curso prático concluído, 50% simulador + 50% no veículo '''
        total_hours_simulator = SystemSettings.objects.all()[0].hours_practical_simulator
        return (self.count_classes_simulator() / total_hours_simulator * 50) + (self.count_classes_car() / self.total_hours * 50)

    def get_absolute_url(self):
        return reverse('process:practical_course', kwargs={'pk_process': self.process.pk})

    class Meta:
        verbose_name = 'Curso prático'
        verbose_name_plural = 'Cursos práticos'

    def __str__(self):
        return 'Curso prático de ' + self.process.student.__str__()

type_hours = {
    'ACC': 20,
    'A': 20,
    'B': 20,
    'AB': 40,
    'C': 20,
    'AC': 40,
    'D': 20,
    'AD': 40,
    'E': 20,
    'AE': 40
}

class Process(models.Model):
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
    student = models.ForeignKey(Student, verbose_name='Aluno', on_delete=models.CASCADE)
    type_cnh = models.CharField('Tipo da CNH', choices=TYPE_CHOICES, max_length=3)

    begin_date = models.DateField('Início', default=datetime.now)
    end_date = models.DateField('Fim', blank=True, null=True, default=None)
    status = models.CharField('Status', max_length=20, default=INICIADO, choices=STATUS_CHOICES)

    exams = models.OneToOneField(Exam, verbose_name='Exames', on_delete=models.CASCADE, blank=True, default=None, null=True)
    theoretical_course = models.OneToOneField(TheoreticalCourse, verbose_name='Curso teórico', on_delete=models.CASCADE, blank=True, default=None, null=True)
    practical_course = models.OneToOneField(PracticalCourse, verbose_name='Curso prático', on_delete=models.CASCADE, blank=True, default=None, null=True)

    def get_percent(self):
        '''Calcula o percentual do processo que o aluno já completou'''
        return int(round(self.exams.get_percent() * 0.2 + self.theoretical_course.get_percent() * 0.3 + self.practical_course.get_percent() * 0.3))

    def __str__(self):
        return 'Proc. #{} -> {}'.format(self.pk, self.student.__str__())

    def get_absolute_url(self):
        return reverse('process:detail_process', kwargs={'pk_process': self.pk})

    class Meta:
        verbose_name = 'Processo'
        verbose_name_plural = 'Processos'
        ordering = ['-begin_date']

class TheoreticalClass(models.Model):
    theoretical_course = models.ForeignKey(TheoreticalCourse, related_name='aulas', verbose_name='Curso teórico', on_delete=models.CASCADE)
    instructor = models.ForeignKey(Employee, verbose_name='Instrutor', on_delete=models.SET_NULL, null=True)
    day = models.DateField('Dia da aula', default=datetime.now)
    begin_time = models.TimeField('Hora do início')
    end_time = models.TimeField('Hora do fim')

    def get_absolute_url(self):
        return self.theoretical_course.get_absolute_url()

    class Meta:
        verbose_name = 'Aula teórica'
        verbose_name_plural = 'Aulas teóricas'

class PracticalClass(models.Model):
    practical_course = models.ForeignKey(PracticalCourse, related_name='aulas', verbose_name='Curso prático', on_delete=models.CASCADE)
    instructor = models.ForeignKey(Employee, verbose_name='Instrutor', on_delete=models.SET_NULL, null=True)
    simulator = models.BooleanField('Aula de simulador', default=False, choices=((True, 'Sim'), (False, 'Não')))
    vehicle = models.ForeignKey(Vehicle, verbose_name='Veículo', on_delete=models.SET_NULL, null=True, blank=True)
    day = models.DateField('Dia da aula', default=datetime.now)
    begin_time = models.TimeField('Hora do início')
    end_time = models.TimeField('Hora do fim')

    def get_absolute_url(self):
        return self.practical_course.get_absolute_url()

    class Meta:
        verbose_name = 'Aula prática'
        verbose_name_plural = 'Aulas práticas'
        # unique_together = (('practical_course', 'day', 'start_time', 'end_time'), ('practical_course', 'day', 'start_time'))

# Signals

def create_process(instance, created, **kwargs):
    if created:
        instance.exams = Exam.objects.create()
        instance.theoretical_course = TheoreticalCourse.objects.create()
        instance.practical_course = PracticalCourse.objects.create()
        instance.save()

def update_end_date(instance, **kwargs):
    # Atualizando a data final do processo: 1 ano
    instance.end_date = date.fromordinal(instance.begin_date.toordinal()+365)
    # Atualizando o total de horas práticas necessárias
    instance.practical_course.total_hours = type_hours[instance.type_cnh]
    instance.practical_course.save()

def update_status_exams(instance, **kwargs):
    if instance.exam_medical and instance.exam_psychological:
        instance.status = CONCLUIDO
    elif instance.exam_medical or instance.exam_psychological:
        instance.status = INICIADO
    else:
        instance.status = NAO_INICIADO

def update_status_theoretical(instance, **kwargs):
    settings = SystemSettings.objects.all()[0]
    course = instance.theoretical_course

    if course.count_classes() >= settings.hours_theoretical:
        course.status = CONCLUIDO
    elif course.count_classes() > 0:
        course.status = INICIADO
    else:
        course.status = NAO_INICIADO
    course.save()

def update_status_practical(instance, **kwargs):
    settings = SystemSettings.objects.all()[0]
    course = instance.practical_course

    if (course.count_classes_simulator() >= settings.hours_practical_simulator) and \
        (course.count_classes_car() >= course.total_hours):
        course.status = CONCLUIDO
    elif (course.count_classes_simulator() > 0) or (course.count_classes_car() > 0):
        course.status = INICIADO
    else:
        course.status = NAO_INICIADO
    course.save()

models.signals.post_save.connect(
    create_process, sender=Process, dispatch_uid='create_process'
)
models.signals.pre_save.connect(
    update_end_date, sender=Process, dispatch_uid='update_end_date'
)
models.signals.pre_save.connect(
    update_status_exams, sender=Exam, dispatch_uid='update_status_exams'
)
models.signals.post_save.connect(
    update_status_theoretical, sender=TheoreticalClass, dispatch_uid='update_status_theoretical'
)
models.signals.post_delete.connect(
    update_status_theoretical, sender=TheoreticalClass, dispatch_uid='update_status_theoretical'
)
models.signals.post_save.connect(
    update_status_practical, sender=PracticalClass, dispatch_uid='update_status_practical'
)
models.signals.post_delete.connect(
    update_status_practical, sender=PracticalClass, dispatch_uid='update_status_practical'
)
