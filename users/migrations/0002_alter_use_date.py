# Generated by Django 4.1.4 on 2022-12-09 12:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='use',
            name='date',
            field=models.DateField(default=datetime.date(2022, 12, 9)),
        ),
    ]
