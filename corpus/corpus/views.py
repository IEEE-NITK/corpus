from django.shortcuts import render
from django.http import HttpResponse
from corpus.tasks import send_email_async

def test_email(request):
    send_email_async.delay(
        subject=f"Test Email",
        template_path="emails/sample_email.html",
        template_context={"name": "user"},
        cc=["serot25764@acedby.com"],
        bcc=["varshini.231cs204@nitk.edu.in"]
    )

    return HttpResponse("<h1>EMAIL SENT</h1>")
