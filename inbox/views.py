from .forms import RegisterMessageForm
from .models import Message
from accounts.models import Person

from core.views.generics import ListView, CreateView

from rolepermissions.mixins import HasPermissionsMixin

class ListMessagesView(HasPermissionsMixin, ListView):
    required_permission = 'student'
    template_name = 'inbox/list_messages_received.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(to__pk=self.request.user.pk)

class RegisterMessageView(HasPermissionsMixin, CreateView):
    required_permission = 'student'
    form_class = RegisterMessageForm
    model = Message
    template_name = 'inbox/register_message.html'

    def get_initials(self):
        return {}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.sender = Person.objects.get(pk=self.request.user.pk)
        self.object.save()
        return super().form_valid(form)

list_messages = ListMessagesView.as_view()
