from django.urls import path
from django.contrib.auth.views import login, logout
from . import views

app_name='core'
urlpatterns = [
    path('', views.index, name='index'),
    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('configuracoes/', views.update_settings, name='update_settings'),
    path('contato/', views.contact, name='contact'),
    path('entrar/', login, {'template_name': 'login.html'}, name='login'),
    path('sair/', logout, {'next_page': 'index'}, name='logout'),
]
