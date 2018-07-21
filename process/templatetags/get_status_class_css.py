from django import template
from process import models

register = template.Library()

@register.filter
def get_class_css(status):
    if status == models.NAO_INICIADO:
        return 'secondary'
    elif status == models.INICIADO:
        return 'info'
    return 'success'
