# Generated by Django 5.0.1 on 2024-04-15 01:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0012_remove_order_image'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='returnorder',
        #     name='id',
        # ),
        migrations.AddField(
            model_name='returnorder',
            name='id_return_order',
            field=models.AutoField(primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
