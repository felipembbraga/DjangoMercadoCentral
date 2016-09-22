from MercadoCentral.viewset import MCReadOnlyModelViewSet
from appdata.models import Product, Section, Highlight
from appdata.serializers import ProductSerializer, SectionSerializer, HighlightSerializer


class ProductViewSet(MCReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # @list_route(methods=['get'])
    # def section_products(self, request, format=None, *args, **kwargs):
    #     section = request.GET.get('section')
    #     reference = request.GET.get('reference')
    #     if not section and not reference:
    #         return self.list(request=request, format=format, *args, **kwargs)
    #     lookups = {}
    #     section and lookups.update({'sections__pk': int(section)}) or None
    #     reference and lookups.update({'sections__reference__exact': reference}) or None
    #     products = self.queryset.filter(**lookups)
    #     page = self.paginate_queryset(products)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(products, many=True)
    #     return Response(serializer.data)


class SectionViewSet(MCReadOnlyModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class HighlightViewSet(MCReadOnlyModelViewSet):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer

