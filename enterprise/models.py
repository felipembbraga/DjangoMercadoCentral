#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class App(models.Model):
    name = models.CharField('nome', max_length=150)
    code = models.CharField(u'código', max_length=100)
    logo = models.ImageField('logomarca', upload_to='app_logo')

    def __unicode__(self):
        return unicode(self.name)

class Contact(models.Model):
    app = models.ForeignKey(App, verbose_name='App')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

