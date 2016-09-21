# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core import serializers
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from MercadoCentral.utils import GetSerializeMixin
from enterprise.models import App

SECTION_TYPES = [
    (0, 'Lista de produtos'),
    (1, 'Página estática'),
    (2, 'Contato'),
]


class ActiveManager(models.Manager):
    def get_queryset(self):
        queryset = super(ActiveManager, self).get_queryset()
        return queryset.filter(is_active=True)


class Section(models.Model):
    enterprise = models.ForeignKey(App, verbose_name='Aplicativo')
    reference = models.CharField(u'referência', max_length=20)
    title = models.CharField(u'título', max_length=50)
    icon = models.CharField(u'ícone', max_length=30, null=True, blank=True)
    type = models.IntegerField(u'tipo', choices=SECTION_TYPES, default=1)
    is_active = models.BooleanField('ativo', default=True)

    class Meta:
        verbose_name = u'Seção'
        verbose_name_plural = u'Seções'
        unique_together = ('enterprise', 'reference')

    def __unicode__(self):
        return self.title


class ActiveSection(Section):
    objects = ActiveManager()

    class Meta:
        proxy = True


class Product(models.Model, GetSerializeMixin):
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
        return self.title

    @property
    def images(self):
        serializer = serializers.serialize('json', self.productimage_set.all(),
                                           fields=('image', 'caption', 'main_image'))
        return self.serialize(serializer)

    def thumbnail(self):
        serializer = serializers.serialize('json', self.productimage_set.filter(main_image=True),
                                           fields=('image', 'caption'))
        return self.serialize(serializer, True)

    @property
    def get_sections(self):
        serializer = serializers.serialize('json', self.sections.all(),
                                           fields=('reference', 'title', 'icon', 'type', 'is_active'))
        return self.serialize(serializer)


class ActiveProduct(Product):
    objects = ActiveManager()

    class Meta:
        proxy = True


def product_directory_path(instance, filename):
    return 'product_{0}/{1}'.format(instance.product.id, filename)

class AppImage(models.Model):
    image = models.ImageField(u'imagem', upload_to=product_directory_path)
    caption = models.CharField(u'legenda', max_length=100)
    main_image = models.BooleanField(u'imagem inicial', default=False)

    class Meta:
        abstract = True

class ProductImage(AppImage):
    product = models.ForeignKey(Product)
    class Meta:
        verbose_name = 'imagem do produto'
        verbose_name_plural = 'imagens do produto'


# signal para contato
@receiver(post_save, sender=ProductImage)
def product_image_post_save(sender, instance, created, **kwargs):
    if not sender.objects.filter(product=instance.product, main_image=True).exists():
        instance.main_image = True
        instance.save()
        return
    if instance.main_image:
        sender.objects.filter(product=instance.product).exclude(pk=instance.pk).update(main_image=False)
        return


class Highlight(models.Model):
    enterprise = models.ForeignKey(App, verbose_name='aplicativo', related_name='app_highlights')
    reference = models.CharField(u'referência', max_length=20)
    title = models.CharField(u'título', max_length=50)
    description = models.TextField(u'descrição', null=True, blank=True)
    is_active = models.BooleanField(u'ativo', default=True)
    section = models.ForeignKey(Section, verbose_name=u'seção', null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name='produto', null=True, blank=True)

    class Meta:
        verbose_name = 'Destaque'

    @property
    def app(self):
        return self.enterprise.name


class HighlightImage(AppImage):
    highlight = models.ForeignKey(Highlight, verbose_name='destaque')

    class Meta:
        verbose_name = 'Imagem para destaque'
        verbose_name_plural = 'Imagens para destaque'


@receiver(post_save, sender=HighlightImage)
def product_image_post_save(sender, instance, created, **kwargs):
    if not sender.objects.filter(product=instance.product, main_image=True).exists():
        instance.main_image = True
        instance.save()
        return
    if instance.main_image:
        sender.objects.filter(product=instance.product).exclude(pk=instance.pk).update(main_image=False)
        return
