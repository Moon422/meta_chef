# Generated by Django 5.0 on 2024-01-03 05:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_kitchen_food_kitchen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='kitchen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.kitchen'),
        ),
    ]
