from django.urls import path
from . import views

app_name='inbox'
urlpatterns = [
    path('mensagens-recebidas/', views.list_messages_received, name='list_messages_received'),
    path('mensagens-enviadas/', views.list_messages_sent, name='list_messages_sent'),
    # Mensagem para qualquer pessoa
    path('enviar-mensagem/<int:person_pk>', views.register_message, name='register_message'),
    # Mensagem com assunto
    path('enviar-mensagem/<int:person_pk>/<str:subject>', views.register_message, name='register_message'),
    path('mensagem/<int:message_pk>', views.detail_message, name='detail_message'),
]
