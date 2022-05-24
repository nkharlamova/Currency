from datetime import datetime, timedelta

from currency import model_choices as mch
from currency.models import Rate, Source
from currency.tasks import round_decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

import requests


class Command(BaseCommand):
    help = 'Parse Privatbank archive rates'

    def handle(self, *args, **options):

        url = 'https://api.privatbank.ua/p24api/exchange_rates'

        last_date = datetime.now(tz=timezone.utc)
        first_date = datetime.now(tz=timezone.utc) - timedelta(days=365 * 4)
        sum_days = (last_date - first_date).days

        available_currencies = {
            'USD': mch.RateType.USD,
            'EUR': mch.RateType.EUR,
            'BTC': mch.RateType.BTC,
            'UAH': mch.RateType.UAH,
        }

        source = Source.objects.get_or_create(code_name=mch.SourceCodeName.PRIVATBANK,
                                              name='PrivatBank')[0]

        for day in range(sum_days):
            date = first_date + timedelta(days=day)
            date_parse_params = {
                'json': '',
                'date': date.strftime("%d.%m.%Y"),
            }

            response = requests.get(url, params=date_parse_params)
            response.raise_for_status()
            rates = response.json()['exchangeRate']

            for cur_type in available_currencies:
                currency_type = available_currencies[cur_type]

                for rate in rates:
                    if ('currency' in rate and
                            cur_type in rate['currency'] and
                            'saleRate' in rate and
                            'purchaseRate' in rate and
                            'baseCurrency' in rate):

                        base_currency_type = available_currencies.get(rate['baseCurrency'])
                        sale = round_decimal(rate['saleRate'])
                        buy = round_decimal(rate['purchaseRate'])

                        try:
                            Rate.objects.get(
                                type=currency_type,
                                base_type=base_currency_type,
                                sale=sale,
                                buy=buy,
                                source=source,
                                created__date=date,  # a lookup to compare a DateTimeField to a date.
                            )
                        except Rate.DoesNotExist:
                            Rate.objects.create(
                                type=currency_type,
                                base_type=base_currency_type,
                                sale=sale,
                                buy=buy,
                                source=source,
                                created=date,  # a record of an archive date
                            )
