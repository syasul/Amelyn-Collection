# Generated by Django 5.0.1 on 2024-04-15 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0012_remove_order_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='returnorder',
            name='id_return_order',
        ),
        migrations.AddField(
            model_name='returnorder',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
