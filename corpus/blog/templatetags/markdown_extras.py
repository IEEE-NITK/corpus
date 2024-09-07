import markdown
from django import template
from django.template import Context
from django.template import Template
from django.utils.safestring import mark_safe

register = template.Library()


# custom filter to convert markdown to html, handles template tags also


@register.filter(name="markdown")
def markdown_to_html(value):
    md_converted_html = markdown.markdown(
        value, extensions=["extra", "codehilite", "toc"]
    )
    t = Template(md_converted_html)
    c = Context({})
    return mark_safe(t.render(c))
