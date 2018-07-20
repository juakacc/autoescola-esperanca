from django.contrib import admin
from django.urls import path, include
from . import views

app_name='process'
urlpatterns = [
    path('', views.list_processes, name='list_processes'),
    path('registro-processo/', views.register_process, name='register_process'),
    path('deletar-processo/<int:pk>', views.delete_process, name='delete_process'),
    path('<int:pk>/', views.detail_process, name='detail_process'),
]
