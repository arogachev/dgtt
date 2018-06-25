from rest_framework import serializers

from .models import Building, Category, Organization


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('id', 'address', 'coordinates')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class OrganizationSerializer(serializers.ModelSerializer):
    building = BuildingSerializer()
    categories = CategorySerializer(many=True)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'phones', 'building', 'categories')
