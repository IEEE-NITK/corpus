from celery import shared_task
from .utils import send_email

@shared_task
def send_email_async(subject, template_path, template_context, cc=None, bcc=None):
    send_email(subject, template_path, template_context, cc, bcc)
