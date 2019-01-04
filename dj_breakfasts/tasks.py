# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .emails import send_deferred_mail

logger = get_task_logger(__name__)

@shared_task
def send_deferred_mail_task(recipient, first_name, date):
    logger.info("Sending breakfast email to {}".format(recipient))
    return send_deferred_mail(recipient, first_name, date)

