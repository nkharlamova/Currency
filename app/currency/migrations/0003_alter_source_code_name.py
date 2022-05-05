# Generated by Django 4.0.2 on 2022-05-03 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0002_rate_base_type_alter_rate_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='code_name',
            field=models.PositiveSmallIntegerField(choices=[(1, 'PrivatBank'), (2, 'MonoBank'), (3, 'Vkurse'), (4, 'OtpBank'), (5, 'UkrsibBank'), (6, 'OschadBank')], unique=True),
        ),
    ]
