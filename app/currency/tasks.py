from decimal import Decimal

from bs4 import BeautifulSoup

from celery import shared_task

from currency import model_choices as mch

import requests


def round_decimal(value: str) -> Decimal:
    places = Decimal(10) ** -2
    return Decimal(value).quantize(places)


@shared_task
def parse_privatbank():
    from currency.models import Rate, Source

    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
        'BTC': mch.RateType.BTC,
        'UAH': mch.RateType.UAH,
    }

    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.PRIVATBANK,
                                          name='PrivatBank', source_url=url)[0]

    for rate in rates:
        currency_type = available_currencies.get(rate['ccy'])
        if not currency_type:
            continue

        base_currency_type = available_currencies.get(rate['base_ccy'])

        sale = round_decimal(rate['sale'])
        buy = round_decimal(rate['buy'])

        last_rate = Rate.objects \
            .filter(source=source, type=currency_type, base_type=base_currency_type) \
            .order_by('-created').first()

        if (last_rate is None or  # does not exist in table
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_monobank():
    from currency.models import Rate, Source

    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        840: mch.RateType.USD,
        978: mch.RateType.EUR,
        980: mch.RateType.UAH,
    }

    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.MONOBANK,
                                          name='MonoBank', source_url=url)[0]

    for rate in rates:
        currency_type = available_currencies.get(rate['currencyCodeA'])
        if not currency_type:
            continue

        base_currency_type = available_currencies.get(rate['currencyCodeB'])

        sale = round_decimal(rate['rateSell'])
        buy = round_decimal(rate['rateBuy'])

        last_rate = Rate.objects \
            .filter(source=source, type=currency_type, base_type=base_currency_type) \
            .order_by('-created').first()

        if (last_rate is None or  # does not exist in table
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_vkurse():
    from currency.models import Rate, Source

    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        'Dollar': mch.RateType.USD,
        'Euro': mch.RateType.EUR,
    }

    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.VKURSE,
                                          name='Vkurse', source_url=url)[0]

    base_currency_type = mch.RateType.UAH

    for rate in rates:
        buy = round_decimal(rates[rate]['buy'])
        sale = round_decimal(rates[rate]['sale'])
        currency_type = rate
        if currency_type not in available_currencies:
            continue

        last_rate = Rate.objects \
            .filter(source=source, type=available_currencies[currency_type]) \
            .order_by('-created') \
            .first()

        if (last_rate is None or  # does not exist in table
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=available_currencies[currency_type],
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_otpbank():
    from currency.models import Rate, Source

    url = 'https://ru.otpbank.com.ua/'
    response = requests.get(url)
    response.raise_for_status()
    main_text = response.text
    soup = BeautifulSoup(main_text, 'lxml')
    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
    }
    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.OTPBANK,
                                          name='OtpBank', source_url=url)[0]

    currency_list_value = soup.find_all('td', {'class': 'currency-list__value'})
    usd_buy = currency_list_value[0].get_text()
    usd_sale = currency_list_value[1].get_text()
    eur_buy = currency_list_value[2].get_text()
    eur_sale = currency_list_value[3].get_text()

    usd = {"type": "USD", "buy": usd_buy, "sale": usd_sale}
    eur = {"type": "EUR", "buy": eur_buy, "sale": eur_sale}

    rates = [usd, eur]

    for rate in rates:
        currency_type = available_currencies.get(rate['type'])
        if not currency_type:
            continue

        base_currency_type = mch.RateType.UAH

        sale = round_decimal(rate['sale'])
        buy = round_decimal(rate['buy'])

        last_rate = Rate.objects \
            .filter(source=source, type=currency_type) \
            .order_by('-created').first()

        if (last_rate is None or  # does not exist in table
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_ukrsibbank():
    from currency.models import Rate, Source

    url = 'https://my.ukrsibbank.com/ru/personal/operations/currency_exchange/'
    response = requests.get(url)
    response.raise_for_status()
    main_text = response.text
    soup = BeautifulSoup(main_text, 'lxml')
    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
    }
    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.UKRSIBBANK,
                                          name='UkrsibBank', source_url=url)[0]

    main_data = soup.find('div', class_='currency__wrapper').find('tbody').findAll('tr')

    rates = []
    for row in main_data:
        raw_string = row.text.strip().split('\n')
        currency = raw_string[0][0:3]
        buy_value = raw_string[1][7:-1]
        sale_value = raw_string[2][7:-1]
        rate_dict = {"type": currency, "buy": buy_value, "sale": sale_value}
        rates.append(rate_dict)

    for rate in rates:
        currency_type = available_currencies.get(rate['type'])
        if not currency_type:
            continue

        base_currency_type = mch.RateType.UAH

        sale = round_decimal(rate['sale'])
        buy = round_decimal(rate['buy'])

        last_rate = Rate.objects \
            .filter(source=source, type=currency_type) \
            .order_by('-created').first()

        if (last_rate is None or  # does not exist in table
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_oschadbank():
    from currency.models import Rate, Source

    url = "https://www.oschadbank.ua/currency-rate"
    response = requests.get(url)
    response.raise_for_status()
    main_text = response.text
    soup = BeautifulSoup(main_text, 'lxml')

    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
    }
    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.OSCHADBANK,
                                          name='OschadBank', source_url=url)[0]

    main_data = soup.find_all(class_="currency__item")

    usd = main_data[1].find_all(class_="currency__item_value")
    eur = main_data[0].find_all(class_="currency__item_value")

    usd_type = main_data[1].find_all(class_="currency__item_name")
    eur_type = main_data[0].find_all(class_="currency__item_name")

    rates = [
        {"type": usd_type[0].get_text(), "buy": usd[0].get_text(), "sale": usd[1].get_text()},
        {"type": eur_type[0].get_text(), "buy": eur[0].get_text(), "sale": eur[1].get_text()}
    ]

    for rate in rates:
        currency_type = available_currencies.get(rate['type'])
        if not currency_type:
            continue

        base_currency_type = mch.RateType.UAH

        sale = round_decimal(rate['sale'])
        buy = round_decimal(rate['buy'])

        last_rate = Rate.objects \
            .filter(source=source, type=currency_type) \
            .order_by('-created').first()

        if (last_rate is None or  # does not exist in table
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )
