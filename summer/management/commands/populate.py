from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from ... import models


cities = (
    ('PPG', 'Pago Pago', 'USA', 'Pacific/Pago_Pago'),
    ('HNL', 'Honolulu', 'USA', 'Pacific/Honolulu'),
    ('ANC', 'Anchorage', 'USA', 'America/Anchorage'),
    ('YVR', 'Vancouver', 'Canada', 'America/Vancouver'),
    ('LAX', 'Los Angeles', 'USA', 'America/Los_Angeles'),
    ('YEA', 'Edmonton', 'Canada', 'America/Edmonton'),
    ('DEN', 'Denver', 'USA', 'America/Denver'),
    ('MEX', 'Mexico City', 'Mexico', 'America/Mexico_City'),
    ('CHI', 'Chicago', 'USA', 'America/Chicago'),
    ('NYC', 'New York City', 'USA', 'America/New_York'),
    ('SCL', 'Santiago', 'Chile', 'America/Santiago'),
    ('YHZ', 'Halifax', 'Canada', 'America/Halifax'),
    ('YYT', "St. John's", 'Canada', 'America/St_Johns'),
    ('RIO', 'Rio de Janeiro', 'Brazil', 'America/Sao_Paulo'),
    ('FEN', 'Fernando de Noronha', 'Brazil', 'America/Noronha'),
    ('RAI', 'Praia', 'Cape Verde', 'Atlantic/Cape_Verde'),
    ('LIS', 'Lisbon', 'Portugal', 'Europe/Lisbon'),
    ('LON', 'London', 'United Kingdom', 'Europe/London'),
    ('MAD', 'Madrid', 'Spain', 'Europe/Madrid'),
    ('PAR', 'Paris', 'France', 'Europe/Paris'),
    ('ROM', 'Rome', 'Italy', 'Europe/Rome'),
    ('BER', 'Berlin', 'Germany', 'Europe/Berlin'),
    ('STO', 'Stockholm', 'Sweden', 'Europe/Stockholm'),
    ('ATH', 'Athens', 'Greece', 'Europe/Athens'),
    ('CAI', 'Cairo', 'Egypt', 'Africa/Cairo'),
    ('JRS', 'Jerusalem', 'Israel', 'Asia/Jerusalem'),
    ('MOW', 'Moscow', 'Russia', 'Europe/Moscow'),
    ('JED', 'Jeddah', 'Saudi Arabia', 'Asia/Riyadh'),
    ('THR', 'Tehran', 'Iran', 'Asia/Tehran'),
    ('DBX', 'Dubai', 'United Arab Emirates', 'Asia/Dubai'),
    ('KBL', 'Kabul', 'Afghanistan', 'Asia/Kabul'),
    ('KHI', 'Karachi', 'Pakistan', 'Asia/Karachi'),
    ('DEL', 'Delhi', 'India', 'Asia/Kolkata'),
    ('KTM', 'Kathmandu', 'Nepal', 'Asia/Kathmandu'),
    ('DAC', 'Dhaka', 'Bangladesh', 'Asia/Dhaka'),
    ('RGN', 'Yangon', 'Burma', 'Asia/Rangoon'),
    ('BKK', 'Bangkok', 'Thailand', 'Asia/Bangkok'),
    ('SIN', 'Singapore', '', 'Asia/Singapore'),
    ('HKG', 'Hong Kong', '', 'Asia/Hong_Kong'),
    ('BJS', 'Beijing', 'China', 'Asia/Shanghai'),
    ('TPE', 'Taipei', 'Taiwan', 'Asia/Taipei'),
    ('SEL', 'Seoul', 'South Korea', 'Asia/Seoul'),
    ('TYO', 'Tokyo', 'Japan', 'Asia/Tokyo'),
    ('ADL', 'Adelaide', 'Australia', 'Australia/Adelaide'),
    ('GUM', 'Guam', '', 'Pacific/Guam'),
    ('SYD', 'Sydney', 'Australia', 'Australia/Sydney'),
    ('NOU', 'Noumea', 'New Caledonia', 'Pacific/Noumea'),
    ('WLG', 'Wellington', 'New Zealand', 'Pacific/Auckland'),
)


class Command(BaseCommand):
    help = 'Create the most common cities'

    def handle(self, *args, **options):
        for iata_code, name, country, timezone in cities:

            try:
                city = models.City.objects.filter(name=name).get()
            except ObjectDoesNotExist:
                city = models.City()
                self.stdout.write(self.style.SUCCESS('Creating ' + name))
            else:
                self.stdout.write(self.style.SUCCESS('Updating ' + name))

            city.iata_code = iata_code
            city.name = name
            city.country = country
            city.timezone = timezone

            city.save()
