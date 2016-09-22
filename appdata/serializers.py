from rest_framework import serializers

from appdata.models import Product, Section, Highlight


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


class HighlightSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Highlight
        fields = ('title', 'description', 'reference', 'is_active', 'product', 'section', 'image', 'link')