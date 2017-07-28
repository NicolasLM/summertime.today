from datetime import datetime, timedelta

import pytz


def get_display_name(user):
    if user.first_name and user.last_name:
        return '{} {}'.format(user.first_name, user.last_name[0])
    return user.username


def is_dst(zonename: str) -> bool:
    """Tell whether a timezone currently has DST enabled."""
    tz = pytz.timezone(zonename)
    now = pytz.utc.localize(datetime.utcnow())
    return now.astimezone(tz).dst() != timedelta(0)


def offset_to_utc(zonename: str) -> int:
    """Give the current offset to UTC of the timezone in seconds."""
    return datetime.now(pytz.timezone(zonename)).utcoffset().total_seconds()


def current_time(zonename: str) -> str:
    return datetime.now(pytz.timezone(zonename)).strftime('%H:%M')
