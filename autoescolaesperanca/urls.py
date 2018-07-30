from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('conta/', include('accounts.urls')),
    path('processos/', include('process.urls')),
    path('mensagens/', include('inbox.urls')),
    path('agenda/', include('diary.urls')),
    path('admin/', admin.site.urls),
]
