# Generated by Django 5.0.1 on 2024-03-09 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0003_alter_order_created_at_alter_orderitem_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2024, 3, 9, 20, 18, 46, 692629, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='returnorder',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2024, 3, 9, 20, 18, 46, 693632, tzinfo=datetime.timezone.utc)),
        ),
    ]
