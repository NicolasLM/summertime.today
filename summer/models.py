import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .utils import is_dst, offset_to_utc, current_time
from .validators import timezone_exists_validator, iata_code_validator


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, blank=True)
    iata_code = models.CharField(max_length=3, unique=True,
                                 validators=(iata_code_validator,))
    timezone = models.CharField(max_length=50,
                                validators=(timezone_exists_validator,))
    has_dst = models.BooleanField(editable=False)
    offset_to_utc = models.IntegerField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('offset_to_utc', 'name')
        verbose_name_plural = 'cities'

    @property
    def time(self):
        return current_time(self.timezone)

    def __str__(self):
        if self.country:
            return '{}, {}'.format(self.name, self.country)
        return self.name


@receiver(pre_save, sender=City)
def populate_city_data_on_create(sender, instance, **kwargs):
    """Set the correct DST and offset when a city is created.

    Only for creation as we do not want to update the DST setting outside of
    tasks because it wouldn't send the email notifications.
    """
    if instance._state.adding:
        instance.has_dst = is_dst(instance.timezone)
        instance.offset_to_utc = offset_to_utc(instance.timezone)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    cities = models.ManyToManyField(City, blank=True)

    def __str__(self):
        return 'Profile of {}'.format(self.user.username)

# Make sure Profile is saved each time User is saved


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
