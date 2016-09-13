from django.shortcuts import render
from rest_framework import viewsets

from enterprise.models import App
from enterprise.serializers import AppSerializer


class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer