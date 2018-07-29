from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy

from core.models import Contact

class IndexView(TemplateView):
    template_name = 'base.html'

class ContactView(SuccessMessageMixin, CreateView):
    template_name = 'contact.html'
    model = Contact
    fields = ['name', 'email', 'subject', 'message']
    success_url = reverse_lazy('core:index')
    success_message = 'Obrigado pelo contato'

class QuemSomosView(TemplateView):
    template_name = 'quem_somos.html'

class localizacaoView(TemplateView):
    template_name = 'localizacao.html'

index = IndexView.as_view()
contact = ContactView.as_view()
quem_somos = QuemSomosView.as_view()
localizacao = localizacaoView.as_view()
