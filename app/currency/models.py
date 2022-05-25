from datetime import datetime

from currency import model_choices as mch

from django.db import models
from django.templatetags.static import static


class ContactUs(models.Model):
    email_from = models.CharField(max_length=100)
    reply_to = models.EmailField(default='')
    subject = models.CharField(max_length=64)
    message = models.CharField(max_length=450)
    created = models.DateTimeField(auto_now_add=True)


class Rate(models.Model):
    type = models.CharField(max_length=5, choices=mch.RateType.choices)
    base_type = models.CharField(max_length=5, choices=mch.RateType.choices, default=mch.RateType.UAH)
    source = models.ForeignKey('currency.Source', on_delete=models.CASCADE, related_name='rates')
    created = models.DateTimeField(default=datetime.now, editable=True)
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.DecimalField(max_digits=10, decimal_places=2)


def upload_logo(instance, filename):
    return f'{instance.name}/logos/{filename}'


class Source(models.Model):
    source_url = models.CharField(max_length=255)
    name = models.CharField(max_length=64, unique=True)
    code_name = models.PositiveSmallIntegerField(choices=mch.SourceCodeName.choices, unique=True)
    logo = models.FileField(upload_to=upload_logo, default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    def logo_url(self):
        if self.logo:
            return self.logo.url

        return static('img/bank.jpg')
