# Generated by Django 4.1.4 on 2022-12-27 08:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_school_code_sch_reg_school_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class_fee',
            name='datey',
            field=models.CharField(default=datetime.date(2022, 12, 27), max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='sch_reg',
            name='date',
            field=models.DateField(default=datetime.date(2022, 12, 27)),
        ),
        migrations.AlterField(
            model_name='use',
            name='date',
            field=models.DateField(default=datetime.date(2022, 12, 27)),
        ),
    ]