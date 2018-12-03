from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy

from core.forms import ContactForm
from core.models import Contact
from core.views.generics import ListView
from news.models import New

class IndexView(ListView):
    paginate_by = 9
    template_name = 'templates_index/index.html'
    model = New

class ContactView(SuccessMessageMixin, CreateView):
    template_name = 'contact.html'
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('core:index')
    success_message = 'Obrigado pelo contato. Retornaremos o mais breve possível!'

class QuemSomosView(TemplateView):
    template_name = 'templates_index/quem_somos.html'

class EquipeView(TemplateView):
    template_name = 'templates_index/equipe.html'

class LocalizacaoView(TemplateView):
    template_name = 'templates_index/localizacao.html'

class FaqView(TemplateView):
    template_name = 'templates_index/faq.html'

index = IndexView.as_view()
contact = ContactView.as_view()
quem_somos = QuemSomosView.as_view()
equipe = EquipeView.as_view()
localizacao = LocalizacaoView.as_view()
faq = FaqView.as_view()
