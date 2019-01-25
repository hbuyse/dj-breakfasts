# -*- coding: utf-8
"""Signals handlers definition."""

# Standard library
import logging
from datetime import date, timedelta

# Third-party
from celery.task.control import revoke

# Django
from django.conf import settings
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

# Current django project
from breakfasts.models import Breakfast, Participant
from breakfasts.tasks import send_deferred_mail_task, create_new_breakfast_task

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Participant)
def post_save_participant(sender, instance, **kwargs):
    """Post saving function used when saving a Participant.

    If the user has just been created, then we create his/her first breakfast.
    If the user has been deactivated, then we remove his/her future breakfasts
    """
    # Add the first breakfast date for a newly created participant.
    if kwargs['created']:
        last_breakfast = Breakfast.objects.last()
        next_friday = date.today() + timedelta((settings.BREAKFAST_DAY - date.today().weekday()) % 7)
        b = Breakfast.objects.create(
            participant=instance,
            date=next_friday if last_breakfast is None else last_breakfast.date + timedelta(weeks=1)
        )
    # If an user is deactivated, then we remove his/her next breakfasts
    elif not instance.is_active:
        q = Breakfast.objects.filter(participant=instance.id, date__gt=date.today())
        for b in q:
            b.delete()


@receiver(pre_save, sender=Breakfast)
def pre_save_breakfast(sender, instance, **kwargs):
    """Prepare the Celery task to send the email and save its id to be remove if needed."""
    if instance.date > date.today():
        email_date = instance.date - timedelta(days=1)

        if len(instance.email_task_id):
            revoke(instance.email_task_id, terminate=True)
            logger.debug("Revoke email send task (id: {})".format(instance.email_task_id))

        task = send_deferred_mail_task.apply_async(
            (
                instance.participant.pk,
                email_date
            ),
            countdown=(email_date - date.today()) / timedelta(seconds=1)
        )
        instance.email_task_id = task.id

        task = create_new_breakfast_task.apply_async(
            (
                instance.participant.pk,
            ),
            countdown=(instance.date - date.today()) / timedelta(seconds=1)
        )
        instance.next_breakfast_task_id = task.id

        logger.info("Breakfast on the date of {} will be payed by {} {}.".format(
            instance.date,
            instance.participant.first_name,
            instance.participant.last_name)
        )
        logger.info("An email (task_id: {}) will be send the {}".format(instance.email_task_id, email_date))


@receiver(post_delete, sender=Breakfast)
def post_delete_breakfast(sender, instance, **kwargs):
    """Anticipate every breakfasts that are after the instance date by a week."""
    q = Breakfast.objects.filter(date__gt=instance.date)

    for b in q:
        logger.info("Moving date of breakfast {} to {}".format(b.date, b.date - timedelta(weeks=1)))
        b.date = b.date - timedelta(weeks=1)
        b.save()
