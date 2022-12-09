# Generated by Django 4.1.4 on 2022-12-08 10:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='fees_update',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_id', models.CharField(default='', max_length=10)),
                ('firstname', models.CharField(max_length=150, null=True)),
                ('middlename', models.CharField(max_length=100, null=True)),
                ('lastname', models.CharField(max_length=100, null=True)),
                ('level', models.CharField(max_length=10, null=True)),
                ('amount', models.FloatField(default='', max_length=12, null=True)),
                ('fee', models.FloatField(default='', max_length=12, null=True)),
                ('balance', models.FloatField(default='', max_length=12, null=True)),
                ('school', models.FloatField(default='', max_length=12, null=True)),
                ('datey', models.DateTimeField(default=django.utils.timezone.now, max_length=40, null=True)),
            ],
        ),
    ]