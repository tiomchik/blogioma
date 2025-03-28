from django.core.mail import EmailMessage
from django.conf import settings

from celery import shared_task


@shared_task
def send_feedback(heading: str, desc: str) -> None:
    sended_email = EmailMessage(
        subject=heading, body=desc,
        from_email=settings.EMAIL_HOST_USER,
        to=[settings.EMAIL_HOST_USER]
    )
    sended_email.send(fail_silently=False)
