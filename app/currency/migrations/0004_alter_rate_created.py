import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('currency', '0003_alter_source_code_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
