# Generated by Django 5.0.1 on 2024-03-01 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0003_alter_cartitem_subtotal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='subtotal',
        ),
    ]
