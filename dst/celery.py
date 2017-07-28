from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

app = Celery('dst')

app.conf.beat_schedule = {
    'check_dst_change': {
        'task': 'summer.tasks.check_dst_change',
        'schedule': crontab(minute='1,16,31,46')
    },
    'check_update_pytz': {
        'task': 'summer.tasks.check_update_pytz',
        'schedule': timedelta(days=2)
    }
}

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

from opbeat.contrib.django.models import client, register_handlers  # noqa
from opbeat.contrib.celery import register_signal  # noqa

register_signal(client)
register_handlers()
