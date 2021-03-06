from django.urls import path
from django.contrib.auth.views import login, logout
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='core'
urlpatterns = [
    path('', views.index, name='index'),
    path('go-home/<str:type>', views.red_home, name='go-home'),
    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('equipe/', views.equipe, name='equipe'),
    path('faq/', views.faq, name='faq'),
    path('localizacao/', views.localizacao, name='localizacao'),
    path('configuracoes/', views.update_settings, name='update_settings'),
    path('contato/', views.contact, name='contact'),
    path('entrar/', login, {'template_name': 'login.html'}, name='login'),
    path('sair/', logout, {'next_page': 'core:index'}, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
