# Generated by Django 4.2.2 on 2024-01-04 07:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_foodviewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodviewed',
            name='view_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 7, 57, 49, 194006, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
