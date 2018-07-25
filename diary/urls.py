from django.urls import path
from . import views

app_name='diary'
urlpatterns = [
    path('listar-agendamento/', views.list_diaries, name='list_diaries'),
    path('listar-agendamento/<str:filter>', views.list_diaries, name='list_diaries'),

    path('registrar-agendamento/', views.register_appointment, name='register_appointment'),
    path('deletar-agendamento/<int:pk>', views.remove_appointment, name='remove_appointment'),
    path('confirmar-agendamento/<int:pk>', views.confirm_appointment, name='confirm_appointment'),
]
