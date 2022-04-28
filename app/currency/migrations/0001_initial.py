# Generated by Django 4.0.2 on 2022-04-27 16:13

import currency.models

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_from', models.CharField(max_length=100)),
                ('reply_to', models.EmailField(default='', max_length=254)),
                ('subject', models.CharField(max_length=64)),
                ('message', models.CharField(max_length=450)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_url', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('code_name',
                 models.PositiveSmallIntegerField(choices=[(1, 'PrivatBank'), (2, 'MonoBank')], unique=True)),
                ('logo', models.FileField(blank=True, default=None, null=True, upload_to=currency.models.upload_logo)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('USD', 'Dollar'), ('EUR', 'Euro')], max_length=5)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('buy', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sale', models.DecimalField(decimal_places=2, max_digits=10)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates',
                                             to='currency.source')),
            ],
        ),
    ]
