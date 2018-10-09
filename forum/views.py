from django.shortcuts import render
from core.views.generics import ListView, DetailView

from django.contrib import messages

from .models import Thread
from .forms import ReplyForm

class ForumView(ListView):

    paginate_by = 2
    template_name = 'forum/index.html'
    model = Thread

    def get_queryset(self):
        queryset = Thread.objects.all()
        order = self.request.GET.get('order', '')

        if order == 'recente':
            queryset = queryset.order_by('-created_at')
        elif order == 'visualizacoes':
            queryset = queryset.order_by('-views')
        elif order == 'comentarios':
            queryset = queryset.order_by('replies')
        return queryset

class ThreadView(DetailView):
    model = Thread
    template_name = 'forum/thread_detail.html'

    def get(self, request, *args, **kwargs):
        ''' Atualiza o número de visualizações '''
        response = super().get(request, *args, **kwargs)

        if self.request.user.is_authenticated and \
            (self.object.author.pk != self.request.user.pk):
            self.object.views = self.object.views + 1
            self.object.save()

        return response

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = ReplyForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = context['form']

        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = self.object
            reply.author = self.request.user
            reply.save()
            messages.success(self.request, 'Resposta enviada com sucesso')
        return self.render_to_response(context)

index = ForumView.as_view()
thread = ThreadView.as_view()
