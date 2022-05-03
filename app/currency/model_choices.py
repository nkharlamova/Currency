from django.db import models


class RateType(models.TextChoices):
    UAH = 'UAH', 'Hryvnia'
    USD = 'USD', 'Dollar'
    EUR = 'EUR', 'Euro'
    BTC = 'BTC', 'Bitcoin'


class SourceCodeName(models.IntegerChoices):
    PRIVATBANK = 1, 'PrivatBank'
    MONOBANK = 2, 'MonoBank'
    VKURSE = 3, 'Vkurse'
    OTPBANK = 4, 'OtpBank'
    UKRSIBBANK = 5, 'UkrsibBank'
    OSCHADBANK = 6, 'OschadBank'
