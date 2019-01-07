from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

import logging

logger = logging.getLogger(__name__)

def send_deferred_mail(recipient, first_name, date):
    if settings.DEBUG:
        logger.info("Mock: send email to {} (to send real email: put settings.DEBUG to True)".format(recipient))
    else:
        to = [recipient]
        from_email = "henri.buyse-ext@sagemcom.com"
        ctx = {
            'first_name': first_name,
            'date': date.strftime("%d/%m/%y")
        }
        subject = render_to_string('dj_breakfasts/email/mail_title.txt', ctx)
        message = render_to_string('dj_breakfasts/email/mail_body.txt', ctx)

        logger.info("Sending breakfast email to {}".format(recipient))
        EmailMessage(subject, message, to=to, from_email=from_email).send()
