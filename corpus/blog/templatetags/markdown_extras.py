import markdown
from django import template
from django.utils.safestring import mark_safe
from django.template import Context,Template

register = template.Library()

# a custom filter to convert markdown to html including support for template tags in the markdown itself
@register.filter(name='markdown')
def markdown_to_html(value):
    md_converted_html = markdown.markdown(value,extensions=['extra','codehilite','toc'])
    t = Template(md_converted_html)
    c = Context({})
    return mark_safe(t.render(c))