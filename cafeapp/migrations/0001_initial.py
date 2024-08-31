# Generated by Django 4.1.7 on 2024-08-29 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('reservation_datetime', models.DateTimeField()),
                ('stay_times', models.IntegerField(default=0)),
                ('remarks', models.CharField(default='', max_length=200)),
                ('is_preorder', models.IntegerField(default=0)),
            ],
        ),
    ]
