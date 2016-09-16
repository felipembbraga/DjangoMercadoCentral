from django.contrib import admin
from django.db import models

from MercadoCentral.widgets import MCAdminImageWidget
from .models import App, Contact
from appdata.models import Section
from MercadoCentral.site import register

class SectionInline(admin.TabularInline):
    model = Section
    extra = 0

class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0

@register(App)
class AppAdmin(admin.ModelAdmin):
    inlines = [ContactInline, SectionInline,]
    list_display = ('name', 'image_tag', 'is_active')
    list_filter = ('is_active',)
    fields = ('name', 'code', 'logo', 'is_active')
    readonly_fields = ('image_tag',)
    formfield_overrides = {
        models.ImageField: {'widget': MCAdminImageWidget}
    }