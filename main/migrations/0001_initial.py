# Generated by Django 4.0.4 on 2022-05-25 18:01

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carriage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.CharField(max_length=120)),
                ('end', models.CharField(max_length=120)),
                ('start_time', models.TimeField(default=datetime.datetime(2022, 5, 25, 18, 1, 46, 951924, tzinfo=utc))),
                ('end_time', models.TimeField()),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lp_station', models.PositiveIntegerField()),
                ('at_location', models.TimeField(default=datetime.datetime(2022, 5, 25, 18, 1, 46, 952917, tzinfo=utc))),
                ('courses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course')),
                ('stations', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.station')),
            ],
        ),
        migrations.CreateModel(
            name='Seating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carriages', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.carriage')),
            ],
        ),
        migrations.AddField(
            model_name='carriage',
            name='courses',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course'),
        ),
    ]
