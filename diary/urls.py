from django.urls import path
from . import views

app_name='diary'
urlpatterns = [
    path('', views.list_diaries, name='list_diaries'),
    path('filtrar/<str:filter>', views.list_diaries, name='list_diaries'),

    path('instrutor/', views.list_diaries_instructor, name='list_diaries_instructor'),
    path('instrutor/<str:filter>', views.list_diaries_instructor, name='list_diaries_instructor'),
    path('aluno/', views.list_diaries_student, name='list_diaries_student'),
    path('aluno/<str:filter>', views.list_diaries_student, name='list_diaries_student'),

    path('<int:pk>/', views.detail_appointment, name='detail_appointment'),
    path('processo/<int:pk_process>', views.list_diaries_process, name='process_appointments'),

    path('registrar-agendamento/', views.register_appointment, name='register_appointment'),
    path('registrar-agendamento/<int:pk_process>', views.register_appointment, name='register_appointment'),
    path('deletar-agendamento/<int:pk>', views.remove_appointment, name='remove_appointment'),
    path('confirmar-agendamento/<int:pk>', views.confirm_appointment, name='confirm_appointment'),
]
