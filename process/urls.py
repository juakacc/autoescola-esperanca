from django.contrib import admin
from django.urls import path, include
from . import views

app_name='process'
urlpatterns = [
    path('', views.list_processes, name='list_processes'),

    path('<int:pk>/', views.detail_process, name='detail_process'),
    path('<int:pk>/atualizar-exames/', views.update_exams, name='update_exams'),
    path('<int:pk>/aulas-teoricas/', views.theoreticals_courses, name='theoreticals_courses'),
    path('registrar-aula-teorica/<int:pk>/', views.register_class, name='register_class_theoretical'),
    # path('<int:pk>/aulas-praticas/', views.practicals_courses, name='practicals_courses'),

    path('registro-processo/', views.register_process, name='register_process'),
    path('deletar-processo/<int:pk>', views.delete_process, name='delete_process'),
]
