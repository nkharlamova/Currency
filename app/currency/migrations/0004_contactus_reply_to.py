# Generated by Django 4.0.2 on 2022-03-31 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0003_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='reply_to',
            field=models.EmailField(default='', max_length=254),
        ),
    ]