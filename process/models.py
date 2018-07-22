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

    def __str__(self):
        return 'Exames de ' + self.process.student.__str__()

class TheoreticalCourse(models.Model):
    status = models.CharField('Status', max_length=20, default=NAO_INICIADO, choices=STATUS_CHOICES)

    # Retorna a quantidade de horas já realizadas
    def count_classes(self):
        aulas, horas = self.aulas.all(), 0

        for aula in aulas:
            hora_aula = datetime.combine(date.min, aula.end_time) - datetime.combine(date.min, aula.start_time)
            horas += (hora_aula.seconds / 3600)
        return horas

    def get_absolute_url(self):
        return reverse('process:theoretical_course', kwargs={'pk_process': self.process.pk})

    class Meta:
        verbose_name = 'Curso teórico'
        verbose_name_plural = 'Cursos teóricos'

    def __str__(self):
        return 'Curso teórico de ' + self.process.student.__str__()

class PracticalCourse(models.Model):
    status = models.CharField('Status', max_length=20, default=NAO_INICIADO, choices=STATUS_CHOICES)

    def count_classes_car(self):
        aulas, horas = self.aulas.filter(simulator=False), 0
        for aula in aulas:
            hora_aula = datetime.combine(date.min, aula.end_time) - datetime.combine(date.min, aula.start_time)
            horas += (hora_aula.seconds / 3600)
        return horas

    def count_classes_simulator(self):
        aulas, horas = self.aulas.filter(simulator=True), 0
        for aula in aulas:
            hora_aula = datetime.combine(date.min, aula.end_time) - datetime.combine(date.min, aula.start_time)
            horas += (hora_aula.seconds / 3600)
        return horas

    def get_absolute_url(self):
        return reverse('process:practical_course', kwargs={'pk_process': self.process.pk})

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
    status = models.CharField('Status', max_length=20, default=INICIADO, choices=STATUS_CHOICES)

    exams = models.OneToOneField(Exam, verbose_name='Exames', on_delete=models.CASCADE, blank=True, default=None, null=True)
    theoretical_course = models.OneToOneField(TheoreticalCourse, verbose_name='Curso teórico', on_delete=models.CASCADE, blank=True, default=None, null=True)
    practical_course = models.OneToOneField(PracticalCourse, verbose_name='Curso prático', on_delete=models.CASCADE, blank=True, default=None, null=True)

    def get_percent(self):
        return 50

    def __str__(self):
        return 'Proc. de ' + self.student.__str__()

    def get_absolute_url(self):
        return reverse('process:detail_process', kwargs={'pk_process': self.pk})

    class Meta:
        verbose_name = 'Processo'
        verbose_name_plural = 'Processos'
        ordering = ['-date_start']

class TheoreticalClass(models.Model):
    theoretical_course = models.ForeignKey(TheoreticalCourse, related_name='aulas', verbose_name='Curso teórico', on_delete=models.CASCADE)
    instructor = models.ForeignKey(Employee, verbose_name='Instrutor', on_delete=models.SET_NULL, null=True)
    day = models.DateField('Dia da aula', default=datetime.now)
    start_time = models.TimeField('Hora do início')
    end_time = models.TimeField('Hora do fim')

    class Meta:
        verbose_name = 'Aula teórica'
        verbose_name_plural = 'Aulas teóricas'

class PracticalClass(models.Model):
    practical_course = models.ForeignKey(PracticalCourse, related_name='aulas', verbose_name='Curso prático', on_delete=models.CASCADE)
    instructor = models.ForeignKey(Employee, verbose_name='Instrutor', on_delete=models.SET_NULL, null=True)
    simulator = models.BooleanField('Aula de simulador', default=False, choices=((True, 'Sim'), (False, 'Não')))
    vehicle = models.ForeignKey(Vehicle, verbose_name='Veículo', on_delete=models.SET_NULL, null=True, blank=True)
    day = models.DateField('Dia da aula', default=datetime.now)
    start_time = models.TimeField('Hora do início')
    end_time = models.TimeField('Hora do fim')

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
    instance.date_end = date.fromordinal(instance.date_start.toordinal()+365)

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
        (course.count_classes_car() >= settings.hours_practical_vehicle):
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
