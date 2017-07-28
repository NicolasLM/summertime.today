from functools import partial

from celery import shared_task, Task
from celery.utils.log import get_task_logger
from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.mail import mail_admins
from django.template.loader import render_to_string
import pytz
import requests

from . import models, utils

logger = get_task_logger(__name__)


class CustomTask(Task):
    """Base Task that enhances the default Task.

    Retries are not sent to Opbeat.
    """

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.warning('Retrying task', exc_info=einfo)


task = partial(shared_task, base=CustomTask, bind=True,
               max_retries=15, default_retry_delay=10,
               autoretry_for=(Exception,))


@task()
@transaction.atomic
def check_dst_change(self):
    """Check if any city enabled/disable DST since last check."""
    changed_cities_id = list()
    cities = models.City.objects.all()

    for city in cities:

        is_dst = utils.is_dst(city.timezone)
        if is_dst == city.has_dst:
            continue

        city.has_dst = is_dst
        city.offset_to_utc = utils.offset_to_utc(city.timezone)
        changed_cities_id.append(str(city.id))
        city.save()

    if changed_cities_id:
        transaction.on_commit(
            lambda: notify_subscribers_of_change.delay(changed_cities_id)
        )


@task()
def notify_subscribers_of_change(self, changed_cities_id):
    """Dispatch sending notifications to interested users."""
    profiles = (
        models.Profile.objects
        .filter(cities__id__in=changed_cities_id)
        .filter(user__emailaddress__verified=True)
        .prefetch_related('cities')
    )

    for profile in profiles:
        cities_id_to_notify = list()
        for city in profile.cities.all():
            if str(city.id) in changed_cities_id:
                cities_id_to_notify.append(city.id)
        send_email_task.delay(profile.user_id, cities_id_to_notify)


@task()
def send_email_task(self, user_id, cities_id):
    user = get_user_model().objects.get(pk=user_id)
    cities = models.City.objects.filter(id__in=cities_id).all()
    display_name = utils.get_display_name(user)

    subject_template = '{}, {} and a few other cities just changed their time'
    template_name = 'summer/email_dst_multi_notification.txt'
    if len(cities) == 1:
        subject_template = '{}, {} just changed its time'
        template_name = 'summer/email_dst_single_notification.txt'

    msg_plain = render_to_string(
        template_name,
        {
            'display_name': display_name,
            'cities': cities
        }
    )
    subject = subject_template.format(display_name, cities[0].name)

    user.email_user(subject, msg_plain)


@task()
def check_update_pytz(self):
    """Notify admins when an update of pytz is available."""
    r = requests.get('https://pypi.python.org/pypi/pytz/json')
    r.raise_for_status()

    new_version = r.json()['info']['version']
    current_version = pytz.VERSION

    if new_version == current_version:
        return

    mail_admins(
        'Update of pytz available {}->{}'.format(current_version, new_version),
        'A new version of pytz is available, you should update it promptly.'
    )
