# Generated by Django 4.1.4 on 2022-12-29 05:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_class_fee_datey_alter_sch_reg_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class_fee',
            name='datey',
            field=models.CharField(default=datetime.date(2022, 12, 29), max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='sch_reg',
            name='date',
            field=models.DateField(default=datetime.date(2022, 12, 29)),
        ),
        migrations.AlterField(
            model_name='use',
            name='date',
            field=models.DateField(default=datetime.date(2022, 12, 29)),
        ),
    ]
