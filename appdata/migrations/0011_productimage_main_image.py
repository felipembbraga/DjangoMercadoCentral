# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-13 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appdata', '0010_auto_20160913_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='main_image',
            field=models.BooleanField(default=False),
        ),
    ]