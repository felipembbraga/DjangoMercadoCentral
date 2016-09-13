#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save

from django.dispatch import receiver


class App(models.Model):
    name = models.CharField('nome', max_length=150)
    code = models.CharField(u'código', max_length=100)
    logo = models.ImageField('logomarca', upload_to='app_logo')
    is_active = models.BooleanField('ativo', default=False)

    def __unicode__(self):
        return unicode(self.name)

class Contact(models.Model):
    app = models.ForeignKey(App, verbose_name='App')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    main_contact = models.BooleanField()

# signal para contato
@receiver(post_save, sender=Contact)
def contact_post_save(sender, instance, created, **kwargs):
    if instance.main_contact:
        sender.objects.filter(app=instance.app).exclude(pk=instance.pk).update(main_contact=False)

