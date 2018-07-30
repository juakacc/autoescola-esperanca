from django.urls import path
from . import views

app_name='inbox'
urlpatterns = [
    path('', views.list_messages, name='list_messages'),
]
