from rest_framework import serializers

from enterprise.models import App


class AppSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = App
        fields = ('name', 'logo', 'code', 'sections')
