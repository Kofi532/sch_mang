# Generated by Django 4.1.4 on 2022-12-20 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_sch_reg_alter_use_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sch_reg',
            name='full_sch',
            field=models.CharField(default='0', max_length=30),
        ),
    ]
