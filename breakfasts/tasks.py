# -*- coding: utf-8 -*-
"""Tasks to be run using celery."""

# Future
from __future__ import absolute_import, unicode_literals

# Standard library
from datetime import timedelta

# Third-party
from celery import shared_task
from celery.utils.log import get_task_logger

# Current django project
from breakfasts.emails import send_deferred_mail
from breakfasts.models import Breakfast, Participant

logger = get_task_logger(__name__)


@shared_task
def send_deferred_mail_task(participant_pk, date):
    """Send an email to the participant.

    The email has to be send 24 hours before the breakfast date to allow the participant to command.
    """
    participant = Participant.objects.get(pk=participant_pk)
    logger.debug("Retrieve participant {} {}".format(participant.first_name, participant.last_name))
    send_deferred_mail(participant.email, participant.first_name, date)


@shared_task
def create_new_breakfast_task(participant_pk):
    """Create a new breakfast the same day the participant as to pay.

    It is not done in the pre_delete signals otherwise we will always have a breakfast date.
    """
    participant = Participant.objects.get(pk=participant_pk)
    last = Breakfast.objects.last()
    Breakfast.objects.create(participant=participant, date=last.date + timedelta(weeks=1))
