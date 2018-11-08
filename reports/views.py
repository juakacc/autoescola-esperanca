from django.shortcuts import render

from core.views.generics import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = 'reports/index_reports.html'

index = IndexView.as_view()
