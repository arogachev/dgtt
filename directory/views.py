from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import Distance
from django.http import JsonResponse

from .models import Organization
from .serializers import OrganizationSerializer


def organizations_by_building(request, building_id):
    organizations = Organization.objects.filter(building__id=building_id).all()
    serializer = OrganizationSerializer(organizations, many=True)
    return JsonResponse(serializer.data, safe=False)


def organizations_by_category(request, category_id):
    organizations = Organization.objects.filter(categories__id=category_id).all()
    serializer = OrganizationSerializer(organizations, many=True)
    return JsonResponse(serializer.data, safe=False)


def organizations_by_radius(request, point, radius):
    distance = Distance(km=radius)
    organizations = Organization.objects.filter(building__coordinates__distance_lte=(point, distance)).all()
    serializer = OrganizationSerializer(organizations, many=True)
    return JsonResponse(serializer.data, safe=False)


def organizations_by_rectangle(request, north_west, south_east):
    x0 = north_west.x
    y0 = south_east.x
    x1 = south_east.y
    y1 = north_west.y
    bbox = (x0, y0, x1, y1)
    polygon = Polygon.from_bbox(bbox)
    organizations = Organization.objects.filter(building__coordinates__coveredby=polygon)
    serializer = OrganizationSerializer(organizations, many=True)
    return JsonResponse(serializer.data, safe=False)
