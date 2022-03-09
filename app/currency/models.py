from django.db import models


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=100)
    subject = models.CharField(max_length=64)
    message = models.CharField(max_length=450)
    created = models.DateTimeField()
