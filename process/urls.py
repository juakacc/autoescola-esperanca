from django.urls import path
from . import views

app_name='process'
urlpatterns = [
    path('', views.list_processes, name='list_processes'),

    path('<int:pk_process>/', views.detail_process, name='detail_process'),
    path('atualizar-processo/<int:pk_process>/', views.update_process, name='update_process'),
    path('<int:pk_process>/atualizar-exames/', views.update_exams, name='update_exams'),

    path('<int:pk_process>/aulas-teoricas/', views.theoretical_course, name='theoretical_course'),
    path('registrar-aula-teorica/<int:pk_course>/', views.register_theoretical_class, name='register_theoretical_class'),
    path('remover-aula-teorica/<int:pk_class>/', views.remove_theoretical_class, name='remove_theoretical_class'),

    path('<int:pk_process>/aulas-praticas/', views.practical_course, name='practical_course'),
    path('registrar-aula-pratica/<int:pk_course>/', views.register_practical_class, name='register_practical_class'),
    path('remover-aula-pratica/<int:pk_class>/', views.remove_practical_class, name='remove_practical_class'),

    path('registro-processo/', views.register_process, name='register_process'),
    path('deletar-processo/<int:pk>', views.delete_process, name='delete_process'),
    # Atualizar processo
]
