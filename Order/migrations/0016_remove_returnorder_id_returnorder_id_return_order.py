# Generated by Django 5.0.1 on 2024-04-15 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0015_remove_returnorder_id_return_order_returnorder_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='returnorder',
            name='id',
        ),
        migrations.AddField(
            model_name='returnorder',
            name='id_return_order',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]