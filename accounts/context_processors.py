from core.models import Contact
from .models import Person

def contacts(context):
    # Adiciona o número de msg não lidas ao contexto do site
    return {
        'num_msg': len(Contact.objects.filter(visualized=False))
    }

def user(context):
    user = context.user
    if user.is_authenticated:
        try:
            person = Person.objects.get(pk=user.pk)
            return {'person': person}
        except:
            return {}
    return {}
