#! /usr/bin/env python

from celery.task.control import revoke
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Breakfast, Participant
from .tasks import send_deferred_mail_task

import logging
from datetime import datetime, date, timedelta

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Participant)
def add_first_breakfast_created_user(sender, instance, **kwargs):
    """Add the first breakfast date for a newly created participant."""
    logger.debug("Post save participant {} {}".format(instance.first_name, instance.last_name));
    if kwargs['created']:
        today = date.today()
        next_friday = today + timedelta( (4-today.weekday()) % 7 ) 
        if today.weekday() == 4:
            next_friday += timedelta(weeks=1)

        logger.info("Creation of the first breakfast at date {}".format(next_friday + timedelta(weeks=len(Participant.objects.filter(is_active=True)))));
        b = Breakfast.objects.create(
                participant=instance,
                date=next_friday + timedelta(weeks=len(Participant.objects.filter(is_active=True)))
            )

@receiver(post_save, sender=Breakfast)
def prepare_send_email(sender, instance, **kwargs):
    email_date = instance.date - timedelta(days=1)

    if not kwargs["created"] and len(instance.email_task_id):
        revoke(instance.email_task_id, terminate=True)
        logger.debug("Revoke email send task (id: {})".format(instance.email_task_id))

    task = send_deferred_mail_task.apply_async(
                (
                    instance.participant.email,
                    instance.participant.first_name,
                    email_date
                ),
                countdown=60
                )
    instance.email_task_id = task.id
    logger.debug("Breakfast on the date of {} will be payed by {} {}.".format(instance.date, instance.participant.first_name, instance.participant.last_name))
    logger.debug("An email (task_id: {}) will be send the {}".format(instance.email_task_id, email_date))
