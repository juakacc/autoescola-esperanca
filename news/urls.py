from django.urls import path
from . import views

app_name='news'
urlpatterns = [
    path('', views.index, name='list_news_edit'),
    path('adicionar', views.register_new, name='register_new'),
    path('deletar-noticia/<int:pk>', views.delete_new, name='delete_new'),
    path('editar-noticia/<int:pk>', views.edit_new, name='edit_new'),
    path('<str:slug>', views.detail_new, name='detail_new')
]
