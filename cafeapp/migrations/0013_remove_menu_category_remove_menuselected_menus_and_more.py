# Generated by Django 4.1.7 on 2024-11-03 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafeapp', '0012_reservation_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='category',
        ),
        migrations.RemoveField(
            model_name='menuselected',
            name='menus',
        ),
        migrations.AddField(
            model_name='menuselected',
            name='menu',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cafeapp.menu'),
            preserve_default=False,
        ),
    ]