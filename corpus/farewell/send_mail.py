from farewell.models import Senior
from corpus.tasks import send_email_async

def send_mails():
    # Get all seniors
    seniors = Senior.objects.all()
    for senior in seniors:
        name = senior.name
        email = senior.email_id
        email = [email]
        url_id = senior.url_id
        url_link = f"https://ieee.nitk.ac.in/farewell/{url_id}"
        send_email_async.delay(
            "",
            "emails/farewell/invite.html",
            {"url_link": url_link, "name": name},
            bcc=email,
        )
        print(f"Email sent to {email}")


send_mails()
