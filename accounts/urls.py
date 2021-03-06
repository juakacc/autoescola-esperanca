from django.urls import path
from . import views
from core import views as core_views

app_name='accounts'
urlpatterns = [
    path('', views.index, name='index'),

    path('funcionarios/', views.list_employees, name='list_employees'),
    path('funcionarios/<str:function>', views.list_employees, name='list_employees'),
    path('funcionario/<int:pk>', views.detail_employee, name='detail_employee'),
    path('deletar-funcionario/<int:pk>', views.delete_employee, name='delete_employee'),
    path('registro-funcionario/', views.register_employee, name='register_employee'),
    path('atualizar-funcionario/<int:pk>', views.update_employee, name='update_employee'),

    path('registro-aluno/', views.register_student, name='register_student'),
    path('atualizar-aluno/<int:pk>', views.update_student, name='update_student'),
    path('alunos/', views.list_students, name='list_students'),
    path('aluno/<int:pk>', views.detail_student, name='detail_student'),
    path('deletar-aluno/<int:pk>', views.delete_student, name='delete_student'),

    path('registro-veiculo/', core_views.register_vehicle, name='register_vehicle'),
    path('atualizar-veiculo/<int:pk>', core_views.update_vehicle, name='update_vehicle'),
    # 0 - funcionando, 1 - em conserto
    path('atualizar-estado-veiculo/<int:pk>/<int:state>', core_views.update_state_vehicle, name='update_state_vehicle'),
    path('deletar-veiculo/<int:pk>', core_views.delete_vehicle, name='delete_vehicle'),
    path('veiculos/', core_views.list_vehicles, name='list_vehicles'),
    path('veiculos/<str:type>', core_views.list_vehicles, name='list_vehicles'),
    path('veiculo/<str:slug>', core_views.detail_vehicle, name='detail_vehicle'),

    path('alterar-dados/', views.update_data, name='update'),
    path('alterar-senha/', views.update_password, name='update_password'),
    path('recuperar-senha/', views.reset_password, name='reset_password'),
    path('definir-senha/<str:key>', views.password_reset_confirm, name='password_reset_confirm'),

    path('contatos/', core_views.messages, name='messages'),
    path('contato/<int:pk>', core_views.message, name='message'),
]
