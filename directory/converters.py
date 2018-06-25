from decimal import *

from django.contrib.gis.geos import Point


class PointConverter:
    regex = '(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)'

    def to_python(self, value):
        return Point(tuple(Decimal(coordinate) for coordinate in value.split(',')))

    def to_url(self, value):
        return value
