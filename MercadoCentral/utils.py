from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from django.core import serializers

class GetSerializeMixin(object):
    def serialize(self, data, first=False):
        return JSONParser().parse(BytesIO(data))