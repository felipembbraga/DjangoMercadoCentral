from rest_framework import serializers

from appdata.models import Product, Section


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id',
                  'reference',
                  'title',
                  'short_description',
                  'description',
                  'is_active',
                  'enterprise',
                  'images',
                  'get_sections',
                  'thumbnail'
                  ]


class SectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Section
        fields = ('reference', 'title', 'icon', 'type', 'is_active')