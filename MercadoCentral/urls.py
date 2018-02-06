"""MercadoCentral URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
from django.views.static import serve
from rest_framework import routers, serializers

from appdata.views import ProductViewSet, SectionViewSet, HighlightViewSet
from enterprise.views import AppViewSet
from .site import site as mc_site


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'apps', AppViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'highlights', HighlightViewSet)

urlpatterns = [
    url(r'^%s$' % settings.BASE_URL, RedirectView.as_view(url='mc_admin', permanent=False)),
    url(r'^%sapi/' % settings.BASE_URL, include(router.urls)),
    url(r'^%sadmin/' % settings.BASE_URL, admin.site.urls),
    url(r'^%smc_admin/' % settings.BASE_URL, mc_site.urls),
    url(r'^%sapi-auth/' % settings.BASE_URL, include('rest_framework.urls', namespace='rest_framework')),
    url(r'^%stinymce/' % settings.BASE_URL, include('tinymce.urls')),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT}),
    ]

    urlpatterns += staticfiles_urlpatterns()
