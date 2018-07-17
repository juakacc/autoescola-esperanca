from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Contact

def index(request):
    return render(request, 'base.html')

class ContactView(SuccessMessageMixin, CreateView):
    template_name = 'contact.html'
    model = Contact
    success_url = reverse_lazy('index')
    fields = ['name', 'email', 'subject', 'message']

    success_message = 'Obrigado pelo contato'

contact = ContactView.as_view()
