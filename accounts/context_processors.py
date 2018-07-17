from core.models import Contact

def contacts(context):
    # Adiciona o número de msg não lidas ao contexto do site
    return {
        'num_msg': len(Contact.objects.filter(visualized=False))
    }
