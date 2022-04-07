from currency import model_choices as mch

from django.db import models


class ContactUs(models.Model):
    email_from = models.CharField(max_length=100)
    reply_to = models.EmailField(default='')
    subject = models.CharField(max_length=64)
    message = models.CharField(max_length=450)
    created = models.DateTimeField(auto_now_add=True)


class Rate(models.Model):
    type = models.CharField(max_length=5, choices=mch.RateType.choices)
    source = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.DecimalField(max_digits=10, decimal_places=2)


class Source(models.Model):
    source_url = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
