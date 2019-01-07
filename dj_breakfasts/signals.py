#! /usr/bin/env python

from celery.task.control import revoke
from django.conf import settings
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .models import Breakfast, Participant
from .tasks import send_deferred_mail_task

import logging
from datetime import datetime, date, timedelta

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Participant)
def add_first_breakfast_created_user(sender, instance, **kwargs):
    """Post saving function used when saving a Participant
    """
    # Add the first breakfast date for a newly created participant.
    if kwargs['created']:
        last_breakfast = Breakfast.objects.last()
        b = Breakfast.objects.create(
                participant=instance,
                date=last_breakfast.date + timedelta(weeks=1)
            )
    # If an user is deactivated, then we remove his/her next breakfasts
    elif not instance.is_active:
        q = Breakfast.objects.filter(participant=instance.id, date__gt=date.today())
        for b in q:
            b.delete()

@receiver(pre_save, sender=Breakfast)
def prepare_send_email(sender, instance, **kwargs):
    if instance.date > date.today():
        email_date = instance.date - timedelta(days=1)

        if len(instance.email_task_id):
            revoke(instance.email_task_id, terminate=True)
            logger.debug("Revoke email send task (id: {})".format(instance.email_task_id))

        task = send_deferred_mail_task.apply_async(
                    (
                        instance.participant.email,
                        instance.participant.first_name,
                        email_date
                    ),
                    countdown=(email_date - date.today()) / timedelta(seconds=1)
                    )

        instance.email_task_id = task.id
        logger.info("Breakfast on the date of {} will be payed by {} {}.".format(instance.date, instance.participant.first_name, instance.participant.last_name))
        logger.info("An email (task_id: {}) will be send the {}".format(instance.email_task_id, email_date))

@receiver(post_delete, sender=Breakfast)
def anticipate_breakfasts_by_a_week(sender, instance, **kwargs):
    """Anticipate every breakfasts that are after the instance date by a week
    """
    q = Breakfast.objects.filter(date__gt=instance.date)

    for b in q:
        logger.info("Moving date of breakfast {} to {}".format(b.date, b.date - timedelta(weeks=1)))
        b.date = b.date - timedelta(weeks=1)
        b.save()
