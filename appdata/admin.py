from django.contrib import admin
from django.urls import reverse
from django.utils.text import slugify
from tinymce.widgets import TinyMCE

from MercadoCentral.site import register
from MercadoCentral.widgets import MCAdminImageWidget, SelectBoxAsRadioWidget
from .models import Section, Product, ProductImage



@register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'enterprise', 'is_active')
    list_filter = ('enterprise__name','is_active')
    search_fields = ('title', 'enterprise__name')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    min_num = 1
    # formfield_overrides = {
    #     models.ImageField: {'widget': MCAdminImageWidget}
    # }

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'image':
            return db_field.formfield(widget=MCAdminImageWidget())
        if db_field.name == 'main_image':
            return db_field.formfield(widget=SelectBoxAsRadioWidget())
        return super(ProductImageInline, self).formfield_for_dbfield(db_field, request, **kwargs)


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'enterprise', 'is_active')
    list_filter = ('enterprise__name','is_active')
    search_fields = ('title', 'description', 'short_description', 'enterprise__name')
    ordering = ('title',)
    filter_horizontal = ('sections', )
    readonly_fields = ['enterprise', 'reference']
    inlines = [ProductImageInline,]
    # formfield_overrides = {
    #     models.TextField: {'widget': TinyMCE}
    # }

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
            return filter(lambda x: x!= 'enterprise', self.readonly_fields)
        return super(ProductAdmin, self).get_readonly_fields(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.reference = slugify(obj.title)
            if Product.objects.filter(reference=obj.reference, enterprise=obj.enterprise).exists():
                obj.reference += '-'
        super(ProductAdmin, self).save_model(request, obj, form, change)













