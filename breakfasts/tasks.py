# -*- coding: utf-8 -*-

# Future
from __future__ import absolute_import, unicode_literals

# Standard library
from datetime import timedelta

# Third-party
from celery import shared_task
from celery.utils.log import get_task_logger

# Django
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Current django project
from breakfasts.emails import send_deferred_mail
from breakfasts.models import Breakfast, Participant

logger = get_task_logger(__name__)

@shared_task
def send_deferred_mail_and_create_new_breakfast_task(participant_pk, date):
    participant = Participant.objects.get(pk=participant_pk)
    logger.debug("Retrieve participant {} {}".format(participant.first_name, participant.last_name))
    send_deferred_mail(participant.email, participant.first_name, date)
    last = Breakfast.objects.last()
    Breakfast.objects.create(participant=participant, date=last.date + timedelta(weeks=1))
