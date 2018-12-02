from django import forms
from process.models import TheoreticalCourse, Process

def validar_carro(form):
    ''' Se a simulator == Não, então um carro deve está selecionado '''
    vehicle, simulator = form.cleaned_data['vehicle'], form.cleaned_data['simulator']
    if not simulator:
        if not vehicle:
            raise forms.ValidationError('Escolha um veículo')
    return vehicle

def validar_end_time(form):
    ''' O horário final de uma aula não pode ser anterior ao horário inicial '''
    begin, end = form.cleaned_data['begin_time'], form.cleaned_data['end_time']
    if begin >= end:
        raise forms.ValidationError('Tempo final não pode ser menor/igual que o tempo inicial')
    return end

def validar_day(form):
    day = form.cleaned_data['day']
    course = TheoreticalCourse.objects.get(pk=form.argumentos['pk_course'])
    begin_day_process = Process.objects.get(pk=course.process.pk).begin_date

    if (begin_day_process > day):
        raise forms.ValidationError('Essa data é anterior ao início do processo : {}'.format(
            begin_day_process
        ))
    return day
