# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-07 12:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_auto_20170806_1422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='answer_field_type',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='answer_validation_regex',
        ),
        migrations.AlterField(
            model_name='answer',
            name='date_answered',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 7, 12, 51, 6, 259567)),
        ),
    ]
