# Generated by Django 5.0.7 on 2024-08-02 15:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yangiliklarapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsmodel',
            name='slug',
        ),
        migrations.AlterField(
            model_name='newsmodel',
            name='body',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='newsmodel',
            name='publish_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 2, 15, 47, 5, 607084, tzinfo=datetime.timezone.utc)),
        ),
    ]
