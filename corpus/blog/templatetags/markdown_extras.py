from django import template
from django.template import Context
from django.template import Template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="render_function")
def render_html(value):
    t = Template(value)

    c = Context({})
    return mark_safe(t.render(c))
