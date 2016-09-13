# -*- coding: utf-8 -*-
from django.contrib.admin.sites import AdminSite

class MCAdminSite(AdminSite):
    site_header = 'Mercado Central'
    site_title = 'Mercado Central - Administração'

site = MCAdminSite(name='mc_admin')

def register(*models, **kwargs):
    """
    Registers the given model(s) classes and wrapped ModelAdmin class with
    admin site:

    @register(Author)
    class AuthorAdmin(admin.ModelAdmin):
        pass

    A kwarg of `site` can be passed as the admin site, otherwise the default
    admin site will be used.
    """
    from django.contrib.admin import ModelAdmin

    def _model_admin_wrapper(admin_class):
        if not models:
            raise ValueError('At least one model must be passed to register.')

        admin_site = kwargs.pop('site', site)

        if not isinstance(admin_site, MCAdminSite):
            raise ValueError('site must subclass MCAdminSite')

        if not issubclass(admin_class, ModelAdmin):
            raise ValueError('Wrapped class must subclass ModelAdmin.')

        admin_site.register(models, admin_class=admin_class)

        return admin_class
    return _model_admin_wrapper