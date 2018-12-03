from django import template
from process import models
from core.constantes import *

register = template.Library()

@register.filter
def get_class_css(status):
    if status == NAO_INICIADO:
        return 'secondary'
    elif status == INICIADO:
        return 'info'
    return 'success'
