# Generated by Django 4.1.7 on 2024-09-02 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafeapp', '0004_rename_reservation_datetime_reservation_datetime_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='customer_name',
        ),
    ]