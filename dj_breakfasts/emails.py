from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import logging

logger = logging.getLogger(__name__)

def send_deferred_mail(recipient, first_name, date):
    subject = "[PETIT DEJ] Le {}, c'est votre tour".format(date.strftime("%d/%m/%y"))
    to = [recipient]
    from_email = "henri.buyse-ext@sagemcom.com"
    ctx = {
        'first_name': first_name,
        'date': date.strftime("%d/%m/%y")
    }
    message = render_to_string('dj_breakfasts/mail_template.txt', ctx)

    EmailMessage(subject, message, to=to, from_email=from_email).send()

    return 4

