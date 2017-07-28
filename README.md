Summertime.today
================

Source of [summertime.today](https://summertime.today), a website that helps
tracking Daylight Saving Time changes. Written in Python 3 with Django and
Celery.

Besides tracking DST, this code shows:

* Integration of Celery 4 into Django
* Social login with django-allauth
* Error reporting and performance monitoring with Opbeat
* Compaction and minification of assets with django-compress

Development
-----------

Create a development `settings_dev.py`, for instance:

```python
DEBUG = True
SECRET_KEY = 'you-know-what-to-put-here'

from dst.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        '...': '...'
    }
}
```

Launch the development server:

    DJANGO_SETTINGS_MODULE=settings_dev ./manage.py runserver

Launch a Celery worker:

    DJANGO_SETTINGS_MODULE=settings_dev celery -A dst -l info worker -B

