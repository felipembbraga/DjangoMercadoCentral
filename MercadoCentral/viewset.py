from rest_framework import viewsets


class MCReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    
    def list(self, request, *args, **kwargs):
        if len(request.GET) > 0:
            lookups = request.GET.dict()
            self.queryset = self.queryset.filter(**lookups)
        return super(MCReadOnlyModelViewSet, self).list(request, *args, **kwargs)