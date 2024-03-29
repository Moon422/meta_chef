# Generated by Django 5.0 on 2024-01-03 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rating_date_created_rating_date_updated_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_charge',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='phonenumber',
            field=models.CharField(default='01748689039', max_length=14),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='date_updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='date_updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='foodcategory',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='foodcategory',
            name='date_updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='date_updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='date_updated',
            field=models.DateField(auto_now=True),
        ),
    ]
