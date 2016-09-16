from django.contrib import admin
from django.db import models

from MercadoCentral.widgets import MCAdminImageWidget
from .models import Section, Product, ProductImage
from MercadoCentral.site import register


@register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'enterprise', 'is_active')
    list_filter = ('enterprise__name','is_active')
    search_fields = ('title', 'enterprise__name')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    min_num = 1
    formfield_overrides = {
        models.ImageField: {'widget': MCAdminImageWidget}
    }


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'enterprise', 'is_active')
    list_filter = ('enterprise__name','is_active')
    search_fields = ('title', 'description', 'short_description', 'enterprise__name')
    ordering = ('title',)
    filter_horizontal = ('sections', )
    inlines = [ProductImageInline,]
