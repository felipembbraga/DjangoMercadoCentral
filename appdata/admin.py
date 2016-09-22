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
from MercadoCentral.widgets import MCAdminImageWidget, SelectBoxAsRadioWidget, ReadOnlyInput, ReadOnlyFormField
from appdata.widgets import IoniconsInput
from enterprise.models import App
from .models import Section, Product, ProductImage, Highlight, HighlightImage


def get_changelist_filter(request):
    url_get = request.GET.get('_changelist_filters')
    return dict((x, y) for x, y in map(lambda x: x.replace('+', ' ').split('='), url_get.split('&')))


def get_formfield(field_name):
    def function(obj, db_field, request):
        initial = obj.get_changeform_initial_data(request)
        if initial.get(field_name):
            field = db_field.formfield(widget=ReadOnlyInput(obj=initial.get(field_name)))
            return field
        return None
    return function

def formfield_for_enterprise(obj, db_field, request):
    initial = obj.get_changeform_initial_data(request)
    if initial.get('enterprise'):
        field = db_field.formfield(widget=ReadOnlyInput(obj=initial.get('enterprise')))
        return field
    return None


class AppFilterListModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super(AppFilterListModelAdmin, self).__init__(model, admin_site)
        self.filters = {}

    def get_changeform_initial_data(self, request):
        initial = super(AppFilterListModelAdmin, self).get_changeform_initial_data(request)
        if not request.GET.get('_changelist_filters'):
            return initial
        self.filters = get_changelist_filter(request)
        if 'enterprise__name' in self.filters.keys():
            enterprise = App.objects.filter(name=unquote(self.filters.get('enterprise__name'))).first()
            if enterprise:
                initial.update({'enterprise': enterprise})
        return initial

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = None
        if hasattr(self, 'formfield_for_%s' % db_field.name):
            field = getattr(self, 'formfield_for_%s' % db_field.name)(db_field, request)
        return field or super(AppFilterListModelAdmin, self).formfield_for_dbfield(db_field=db_field, request=request, **kwargs)


class EnterpriseFilter(admin.FieldListFilter):
    def expected_parameters(self):
        return [self.parameter_name]

    def choices(self, changelist):
        pass

    title = 'Por app'
    parameter_name = 'enterprise__name'


class ImageInline(admin.TabularInline):
    extra = 0
    min_num = 1

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'image':
            return db_field.formfield(widget=MCAdminImageWidget())
        if db_field.name == 'main_image':
            return db_field.formfield(widget=SelectBoxAsRadioWidget())
        return super(ImageInline, self).formfield_for_dbfield(db_field, request, **kwargs)


@register(Section)
class SectionAdmin(AppFilterListModelAdmin):
    list_display = ('title', 'enterprise', 'is_active')
    list_filter = ('enterprise__name', 'is_active')
    search_fields = ('title', 'enterprise__name')
    readonly_fields = ['enterprise']

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        return super(SectionAdmin, self).render_change_form(request, context, add, change, form_url, obj)

    formfield_for_enterprise = get_formfield('enterprise')

    def formfield_for_icon(self, db_field, *args, **kwargs):
        return db_field.formfield(widget=IoniconsInput())

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


class ProductImageInline(ImageInline):
    model = ProductImage


@register(Product)
class ProductAdmin(AppFilterListModelAdmin):
    list_display = ('title', 'short_description', 'enterprise', 'is_active')
    list_filter = ('enterprise__name', 'is_active')
    search_fields = ('title', 'description', 'short_description', 'enterprise__name')
    ordering = ('title',)
    filter_horizontal = ('sections',)
    readonly_fields = ['enterprise', 'reference']
    inlines = [ProductImageInline, ]

    formfield_for_enterprise = get_formfield('enterprise')

    def formfield_for_description(self, db_field, *args, **kwargs):
        return db_field.formfield(widget=TinyMCE(
            attrs={'cols': 80, 'rows': 15},
            mce_attrs={'external_link_list_url': reverse('tinymce-linklist')},
        ))

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


class HighlightImageInline(ImageInline):
    model = HighlightImage


@register(Highlight)
class HighlightAdmin(AppFilterListModelAdmin):
    list_display = ('title', 'description', 'enterprise', 'section', 'product', 'is_active')
    list_filter = (
        'enterprise__name',
        'section',
        'is_active'
    )
    # inlines = [HighlightImageInline, ]

    def get_changeform_initial_data(self, request):
        initial = super(HighlightAdmin, self).get_changeform_initial_data(request)
        if 'section__id__exact' in self.filters.keys():
            section = Section.objects.filter(pk=unquote(self.filters.get('section__id__exact'))).first()
            if section:
                initial.update({'section': section})
        return initial

    def get_form(self, request, obj=None, **kwargs):
        form = super(HighlightAdmin, self).get_form(request, obj, **kwargs)
        if obj is not None:
            form.base_fields['section'].queryset = Section.objects.filter(enterprise=obj.enterprise)
        else:
            initial = self.get_changeform_initial_data(request)
            if initial.get('enterprise'):
                form.base_fields['section'].queryset = Section.objects.filter(enterprise=initial.get('enterprise'))
                form.base_fields['product'].queryset = Product.objects.filter(enterprise=initial.get('enterprise'))

        return form

    formfield_for_enterprise = get_formfield('enterprise')
    formfield_for_section = get_formfield('section')
