from django.db import models


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=100)
    subject = models.CharField(max_length=64)
    message = models.CharField(max_length=450)
    created = models.DateTimeField()


class Rate(models.Model):
    type = models.CharField(max_length=5)
    source = models.CharField(max_length=64)
    created = models.DateTimeField()
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.DecimalField(max_digits=10, decimal_places=2)


class Source(models.Model):
    source_url = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
