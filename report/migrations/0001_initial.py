# Generated by Django 4.1.4 on 2022-12-27 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_id', models.CharField(default=0, max_length=30, null=True)),
                ('subjectA', models.CharField(default=0, max_length=10, null=True)),
                ('subjectB', models.CharField(default=0, max_length=10, null=True)),
                ('subjectC', models.CharField(default=0, max_length=10, null=True)),
                ('subjectD', models.CharField(default=0, max_length=10, null=True)),
                ('subjectE', models.CharField(default=0, max_length=10, null=True)),
                ('subjectF', models.CharField(default=0, max_length=10, null=True)),
                ('subjectG', models.CharField(default=0, max_length=10, null=True)),
                ('subjectH', models.CharField(default=0, max_length=10, null=True)),
                ('subjectI', models.CharField(default=0, max_length=10, null=True)),
                ('subjectJ', models.CharField(default=0, max_length=10, null=True)),
                ('subjectK', models.CharField(default=0, max_length=10, null=True)),
                ('subjectL', models.CharField(default=0, max_length=10, null=True)),
                ('school', models.FloatField(default=0, max_length=10, null=True)),
            ],
        ),
    ]
