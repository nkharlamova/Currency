# Generated by Django 4.0.2 on 2022-03-19 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0002_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_url', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
    ]
