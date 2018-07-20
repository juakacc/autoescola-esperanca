from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import login, logout
from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contato/', views.contact, name='contact'),
    path('conta/', include('accounts.urls')),
    path('processos/', include('process.urls')),
    path('entrar/', login, {'template_name': 'login.html'}, name='login'),
    path('sair/', logout, {'next_page': 'index'}, name='logout'),
    path('admin/', admin.site.urls),
]
