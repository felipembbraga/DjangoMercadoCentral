from django.contrib import admin
from django.utils.text import slugify

from MercadoCentral.site import register
from MercadoCentral.widgets import MCAdminImageWidget, BRPhoneInput
from appdata.models import Section
from appdata.widgets import IoniconsInput
from enterprise.models import App, Contact
from MercadoCentral.widgets import SelectBoxAsRadioWidget


class SectionInline(admin.TabularInline):
    model = Section
    extra = 0
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'icon':
            return db_field.formfield(widget=IoniconsInput())
        return super(SectionInline, self).formfield_for_dbfield(db_field, request, **kwargs)


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'phone':
            return db_field.formfield(widget=BRPhoneInput(mask={'mask': '(99)99999-9999'}))
        if db_field.name == 'main_contact':
            return db_field.formfield(widget=SelectBoxAsRadioWidget())
        return super(ContactInline, self).formfield_for_dbfield(db_field, request, **kwargs)


@register(App)
class AppAdmin(admin.ModelAdmin):
    inlines = [ContactInline, ]
    list_display = ('name', 'image_tag', 'is_active')
    list_filter = ('is_active',)
    fields = ('name', 'code', 'logo', 'is_active')
    readonly_fields = ('code',)
    # change_form_template = 'enterprise_admin/change_form.html'

    def get_inline_instances(self, request, obj=None):
        return obj and super(AppAdmin, self).get_inline_instances(request, obj) or []

    def get_fields(self, request, obj=None):
        fields = super(AppAdmin, self).get_fields(request, obj)
        if obj is None:
            return filter(lambda x: x != 'code', fields)
        return fields

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'logo':
            return db_field.formfield(widget=MCAdminImageWidget())
        return super(AppAdmin, self).formfield_for_dbfield(db_field, request, **kwargs)



