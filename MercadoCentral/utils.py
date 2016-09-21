import urllib2

from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from django.core import serializers


class GetSerializeMixin(object):
    @staticmethod
    def serialize(data, first=False):
        return JSONParser().parse(BytesIO(data))


def unquote(string):
    return urllib2.unquote(string).encode('latin1').decode('utf-8')