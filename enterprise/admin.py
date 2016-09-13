from django.contrib import admin
from .models import App, Contact
from appdata.models import Section

class SectionInline(admin.TabularInline):
    model = Section
    extra = 0

class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    inlines = [ContactInline, SectionInline,]
    list_display = ('name', 'logo', 'is_active')
    list_filter = ('is_active',)
