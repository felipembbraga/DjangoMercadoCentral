# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core import serializers
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from enterprise.models import App

SECTION_TYPES = [
    (0, 'Lista de produtos'),
    (1, 'Página estática'),
    (2, 'Contato'),
]


class Section(models.Model):
    enterprise = models.ForeignKey(App, verbose_name='Aplicativo')
    reference = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    icon = models.CharField(max_length=30, null=True, blank=True)
    type = models.IntegerField(choices=SECTION_TYPES, default=1)
    is_active = models.BooleanField('ativo', default=True)

    class Meta:
        verbose_name = u'Seção'
        verbose_name_plural = u'Seções'

    def __unicode__(self):
        return unicode(self.title)


class Product(models.Model):
    enterprise = models.ForeignKey(App, verbose_name='Aplicativo')
    reference = models.CharField(u'referência', max_length=20)
    title = models.CharField(u'título', max_length=50)
    short_description = models.CharField(u'descrição breve', max_length=120, null=True, blank=True)
    description = models.TextField(u'Descrição', null=True, blank=True)
    is_active = models.BooleanField(u'ativo', default=True)
    sections = models.ManyToManyField(Section, verbose_name=u'seções')

    class Meta:
        verbose_name = u'Produto'
        unique_together = ('enterprise', 'reference')

    def __unicode__(self):
        return unicode(self.title)

    def get_images(self):
        return serializers.serialize('json', self.productimage_set.all(), fields=('image', 'caption', 'main_image'))


def product_directory_path(instance, filename):
    return 'product_{0}/{1}'.format(instance.product.id, filename)


class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(u'imagem', upload_to=product_directory_path)
    caption = models.CharField(u'legenda', max_length=100)
    main_image = models.BooleanField(u'imagem inicial', default=False)

    class Meta:
        verbose_name = 'imagem do produto'
        verbose_name_plural = 'imagens do produto'


# signal para contato
@receiver(post_save, sender=ProductImage)
def contact_post_save(sender, instance, created, **kwargs):
    if instance.main_image:
        sender.objects.filter(product=instance.product).exclude(pk=instance.pk).update(main_image=False)
