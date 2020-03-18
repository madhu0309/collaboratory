from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@task(name="sum_two_numbers")
def add(x, y):
    return x + y


@task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total


@task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)


@task
def abcsum(numbers):
    return sum(numbers)


@task
def send_email_user_answer(
    user_email, added_by="", domain="demo.django-crm.io", protocol="http"
):
    """ Send Mail To Users When their account is deleted """
    if user_email:
        context = {}
        context["message"] = "added question"
        context["deleted_by"] = added_by
        context["email"] = user_email
        recipients = []
        recipients.append(user_email)
        subject = "Collaboratory : Answer is added to your question. "
        html_content = render_to_string("user_added_question.html", context=context)
        if recipients:
            msg = EmailMessage(subject, html_content, to=recipients)
            msg.content_subtype = "html"
            msg.send()
