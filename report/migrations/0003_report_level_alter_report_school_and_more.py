# Generated by Django 4.1.4 on 2022-12-28 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_report_number_alter_report_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='level',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='school',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='subjectA',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='subjectB',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='subjectC',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='subjectD',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='subjectE',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='subjectF',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='subjectG',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='subjectH',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='subjectI',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='subjectJ',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='subjectK',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='subjectL',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
    ]
