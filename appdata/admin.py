from __future__ import unicode_literals

import json

from django.conf.urls import url
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.text import slugify
from tinymce.widgets import TinyMCE

from MercadoCentral.site import register
from MercadoCentral.utils import unquote
from MercadoCentral.widgets import MCAdminImageWidget, SelectBoxAsRadioWidget
from appdata.widgets import IoniconsInput
from enterprise.models import App
from .models import Section, Product, ProductImage


def get_changelist_filter(request):
    url_get = request.GET.get('_changelist_filters')
    return dict((x, y) for x, y in map(lambda x: x.replace('+', ' ').split('='), url_get.split('&')))


class AppFilterListModelAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        initial = super(AppFilterListModelAdmin, self).get_changeform_initial_data(request)
        if not request.GET.get('_changelist_filters'):
            return initial
        filters = get_changelist_filter(request)
        for key in filters.keys():
            if key == 'enterprise__name':
                enterprise = App.objects.filter(name=unquote(filters.get(key))).first()
                if enterprise:
                    initial.update({'enterprise': enterprise})
        return initial


@register(Section)
class SectionAdmin(AppFilterListModelAdmin):
    list_display = ('title', 'enterprise', 'is_active')
    list_filter = ('enterprise__name', 'is_active')
    search_fields = ('title', 'enterprise__name')
    readonly_fields = ['enterprise']

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        return super(SectionAdmin, self).render_change_form(request, context, add, change, form_url, obj)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'icon':
            return db_field.formfield(widget=IoniconsInput())
        return super(SectionAdmin, self).formfield_for_dbfield(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return filter(lambda x: x != 'enterprise', self.readonly_fields)
        return super(SectionAdmin, self).get_readonly_fields(request, obj)

    def get_urls(self):
        urls = super(SectionAdmin, self).get_urls()
        my_urls = [
            url(r'^icon_list/$', self.icon_list_view, name='icon-list'),
        ]
        # raise Exception(my_urls)
        return my_urls + urls
        return urls

    def icon_list_view(self, request):
        from django.conf import settings
        import os
        filepath = os.path.join(settings.BASE_DIR, 'ionicons.json')

        with open(filepath, 'r') as json_file:
            data = json.load(json_file)
            ionicons = data.get('classes')
            context = dict(
                self.admin_site.each_context(request),
                ionicons=ionicons
            )
            return TemplateResponse(request, 'list_icons.html', context)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    min_num = 1

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'image':
            return db_field.formfield(widget=MCAdminImageWidget())
        if db_field.name == 'main_image':
            return db_field.formfield(widget=SelectBoxAsRadioWidget())
        return super(ProductImageInline, self).formfield_for_dbfield(db_field, request, **kwargs)


@register(Product)
class ProductAdmin(AppFilterListModelAdmin):
    list_display = ('title', 'short_description', 'enterprise', 'is_active')
    list_filter = ('enterprise__name', 'is_active')
    search_fields = ('title', 'description', 'short_description', 'enterprise__name')
    ordering = ('title',)
    filter_horizontal = ('sections',)
    readonly_fields = ['enterprise', 'reference']
    inlines = [ProductImageInline, ]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'description':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 15},
                mce_attrs={'external_link_list_url': reverse('tinymce-linklist')},
            ))
        return super(ProductAdmin, self).formfield_for_dbfield(db_field, request, **kwargs)

    def get_inline_instances(self, request, obj=None):
        return obj and super(ProductAdmin, self).get_inline_instances(request, obj) or []

    def get_fields(self, request, obj=None):
        fields = super(ProductAdmin, self).get_fields(request, obj)
        if obj is None:
            return filter(lambda x: x not in ['sections', 'reference'], fields)
        return fields

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
        if obj is not None:
            form.base_fields['sections'].queryset = Section.objects.filter(enterprise=obj.enterprise)
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return filter(lambda x: x != 'enterprise', self.readonly_fields)
        return super(ProductAdmin, self).get_readonly_fields(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.reference = slugify(obj.title)
            if Product.objects.filter(reference=obj.reference, enterprise=obj.enterprise).exists():
                obj.reference += '-'
        super(ProductAdmin, self).save_model(request, obj, form, change)
