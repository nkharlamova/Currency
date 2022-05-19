from unittest.mock import MagicMock

from currency.models import Rate
from currency.tasks import parse_monobank, parse_privatbank, parse_vkurse


def test_parse_privatbank(mocker):
    response_json = [
        {"ccy": "USD", "base_ccy": "UAH", "buy": "29.25490", "sale": "32.05128"},
        {"ccy": "EUR", "base_ccy": "UAH", "buy": "30.74540", "sale": "33.55705"},
        {"ccy": "RUR", "base_ccy": "UAH", "buy": "0.32000", "sale": "0.35001"},
        {"ccy": "BTC", "base_ccy": "USD", "buy": "27913.8203", "sale": "30852.1171"},
    ]
    request_get_mock = mocker.patch(
        'requests.get', return_value=MagicMock(json=lambda: response_json)
    )

    assert request_get_mock.call_count == 0

    # first exec
    rate_initial_count = Rate.objects.count()
    parse_privatbank()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock.call_count == 1

    # second exec no changes
    parse_privatbank()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock.call_count == 2
    assert request_get_mock.call_args[0] == ('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11',)
    assert request_get_mock.call_args[1] == {}

    # third, change one rate
    response_json = [
        {"ccy": "USD", "base_ccy": "UAH", "buy": "999", "sale": "32.05128"},
    ]
    request_get_mock_2 = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    assert request_get_mock_2.call_count == 0
    parse_privatbank()
    assert Rate.objects.count() == rate_initial_count + 4
    assert request_get_mock_2.call_count == 1


def test_parse_monobank(mocker):
    response_json = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1652908207, "rateBuy": 29.5, "rateSell": 31.5},
        {"currencyCodeA": 978, "currencyCodeB": 980, "date": 1652956207, "rateBuy": 30.9, "rateSell": 33.35},
        {"currencyCodeA": 978, "currencyCodeB": 840, "date": 1652908207, "rateBuy": 1.04, "rateSell": 1.06},
    ]
    request_get_mock = mocker.patch(
        'requests.get', return_value=MagicMock(json=lambda: response_json)
    )

    assert request_get_mock.call_count == 0

    # first exec
    rate_initial_count = Rate.objects.count()
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock.call_count == 1

    # second exec no changes
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock.call_count == 2
    assert request_get_mock.call_args[0] == ('https://api.monobank.ua/bank/currency',)
    assert request_get_mock.call_args[1] == {}

    # third, change one rate
    response_json = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1652908207, "rateBuy": 999, "rateSell": 31.5},
    ]
    request_get_mock_2 = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    assert request_get_mock_2.call_count == 0
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 4
    assert request_get_mock_2.call_count == 1


def test_parse_vkurse(mocker):
    response_json = {
        "Dollar": {"buy": "32.15", "sale": "38.00"},
        "Euro": {"buy": "38.00", "sale": "40.00"},
        "Rub": {"buy": "00.00", "sale": "00.00"},
    }

    request_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json)
    )

    assert request_get_mock.call_count == 0

    # first exec
    rate_initial_count = Rate.objects.count()
    parse_vkurse()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 1

    # second exec no changes
    parse_vkurse()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 2
    assert request_get_mock.call_args_list[0][0] == ('http://vkurse.dp.ua/course.json',)
    assert request_get_mock.call_args[1] == {}

    # third, change one rate
    response_json = {
        "Dollar": {"buy": "999.0", "sale": "38.00"},
        "Euro": {"buy": "38.00", "sale": "40.00"},
        "Rub": {"buy": "00.00", "sale": "00.00"},
    }
    request_get_mock_2 = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    assert request_get_mock_2.call_count == 0
    parse_vkurse()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock_2.call_count == 1
