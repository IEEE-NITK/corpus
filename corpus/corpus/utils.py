from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_email(subject, template_path, template_context, cc=None, bcc=None):
    msg_html = render_to_string(template_path, template_context)
    msg_plain = strip_tags(msg_html)

    msg = EmailMultiAlternatives(
        subject,
        msg_plain,
        "corpusieeenitk@gmail.com",
        ["corpusieeenitk@gmail.com"],
        cc=cc,
        bcc=bcc,
        reply_to=["corpusieeenitk@gmail.com"],
    )
    msg.attach_alternative(msg_html, "text/html")
    msg.send(fail_silently=True)
