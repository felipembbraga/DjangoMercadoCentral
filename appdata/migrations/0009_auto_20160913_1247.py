# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-13 12:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0005_auto_20160913_1220'),
        ('appdata', '0008_auto_20160913_1244'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('enterprise', 'reference')]),
        ),
    ]
