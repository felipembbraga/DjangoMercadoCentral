from django.contrib import admin
from .models import Section

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('enterprise', 'title', 'is_active')
    list_filter = ('enterprise',)

# Register your models here.
