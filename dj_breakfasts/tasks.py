# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

logger = get_task_logger(__name__)

@shared_task
def send_deferred_mail(recipient, first_name, date):
    logger.info("Sending breakfast email to {}".format(recipient))
    subject = "[PETIT DEJ] Le {}, c'est votre tour".format(date)
    to = [recipient]
    from_email = "henri.buyse-ext@sagemcom.com"
    ctx = {
        'first_name': first_name,
        'date': date
    }
    message = render_to_string('dj_breakfasts/mail_template.txt', ctx)

    EmailMessage(subject, message, to=to, from_email=from_email).send()

    return 4

