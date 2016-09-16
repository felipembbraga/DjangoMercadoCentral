# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core import serializers
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from MercadoCentral.utils import GetSerializeMixin


class App(models.Model, GetSerializeMixin):
    name = models.CharField('nome', max_length=150)
    code = models.CharField(u'código', max_length=100)
    logo = models.ImageField('logomarca', upload_to='app_logo')
    is_active = models.BooleanField('ativo', default=False)

    def __unicode__(self):
        return unicode(self.name)

    def image_tag(self):
        if not self.logo:
            return ''

        return mark_safe(u'<img src="%s" width="100"/>' % (settings.MEDIA_URL + str(self.logo)))

    @property
    def sections(self):
        serializer = serializers.serialize('json', self.section_set.all(),
                                           fields=('reference', 'title', 'icon', 'type', 'is_active'))
        return self.serialize(serializer)

    image_tag.short_description = 'Logomarca'


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
