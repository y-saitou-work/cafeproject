# Generated by Django 4.1.7 on 2024-09-09 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafeapp', '0009_rename_name_category_category_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='img',
        ),
    ]
