# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core import serializers
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from MercadoCentral.utils import GetSerializeMixin


class App(models.Model, GetSerializeMixin):
    name = models.CharField('nome', max_length=150)
    code = models.CharField(u'código', max_length=100, blank=True)
    logo = models.ImageField('logomarca', upload_to='app_logo')
    is_active = models.BooleanField('ativo', default=True)

    def __unicode__(self):
        return unicode(self.name)

    def image_tag(self):
        if not self.logo:
            return ''

        return mark_safe(u'<img src="%s" width="100"/>' % (settings.MEDIA_URL + str(self.logo)))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.logo or self.logo == '':
            self.logo = slugify(self.name)
        super(App, self).save(force_insert, force_update, using, update_fields)

    @property
    def sections(self):
        serializer = serializers.serialize('json', self.section_set.all(),
                                           fields=('reference', 'title', 'icon', 'type', 'is_active'))
        return self.serialize(serializer)

    image_tag.short_description = 'Logomarca'


class Contact(models.Model):
    app = models.ForeignKey(App, verbose_name='App')
    name = models.CharField('nome', max_length=100)
    phone = models.CharField('telefone', max_length=15)
    email = models.EmailField('email')
    main_contact = models.BooleanField('contato principal')

    class Meta:
        verbose_name='Contato'
        verbose_name_plural='Contatos'


# signal para contato
@receiver(post_save, sender=Contact)
def contact_post_save(sender, instance, created, **kwargs):
    if instance.main_contact:
        sender.objects.filter(app=instance.app).exclude(pk=instance.pk).update(main_contact=False)
