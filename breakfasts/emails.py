import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

def send_deferred_mail(recipient, first_name, date):
    if recipient is None or first_name is None or date is None:
        return False

    to = [recipient]
    from_email = "henri.buyse-ext@sagemcom.com"
    ctx = {
        'first_name': first_name,
        'date': date.strftime("%d/%m/%y")
    }
    subject = render_to_string('breakfasts/email/mail_title.txt', ctx)
    message = render_to_string('breakfasts/email/mail_body.txt', ctx)

    logger.info("Sending breakfast email to {}".format(recipient))
    EmailMessage(subject, message, to=to, from_email=from_email).send()

    return True