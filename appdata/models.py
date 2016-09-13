#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from enterprise.models import App, Contact

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
    is_active = models.BooleanField(default=True)
    class Meta:
        verbose_name = u'Seção'
        verbose_name_plural = u'Seções'


class Product(models.Model):
    enterprise = models.ForeignKey(App, verbose_name='Aplicativo')
    reference = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    short_description = models.CharField(max_length=120)
    description = models.TextField()

def product_directory_path(instance, filename):
    return 'product_{0}/{1}'.format(instance.product.id, filename)

class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=product_directory_path)
    caption = models.CharField(max_length=100)