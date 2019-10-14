from __future__ import absolute_import, unicode_literals
from django.utils.html import strip_tags
from celery import shared_task, task
from django.core.mail import EmailMultiAlternatives


@task
def send_confirmation_email(message, to_email):
    subject, from_email, to = 'فعال سازی اکانت InfoBloG', 'noreply@example.com', to_email

    text_content = strip_tags(message)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(message, 'text/html')
    msg.send()
