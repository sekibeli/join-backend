# Generated by Django 4.2.6 on 2023-10-14 16:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joinbackendapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateField(default=datetime.date.today),
        ),
    ]