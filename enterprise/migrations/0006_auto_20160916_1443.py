# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-16 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0005_auto_20160913_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='ativo'),
        ),
    ]
