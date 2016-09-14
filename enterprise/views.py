from rest_framework import viewsets

from MercadoCentral.viewset import MCReadOnlyModelViewSet
from enterprise.models import App
from enterprise.serializers import AppSerializer


class AppViewSet(MCReadOnlyModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer