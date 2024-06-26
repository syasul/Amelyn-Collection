# Generated by Django 5.0.1 on 2024-03-09 20:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0002_order_created_at_order_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2024, 3, 9, 20, 17, 51, 783996, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='returnorder',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2024, 3, 9, 20, 17, 51, 785001, tzinfo=datetime.timezone.utc)),
        ),
    ]
