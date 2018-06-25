from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Building(models.Model):
    address = models.CharField(max_length=75, unique=True)
    coordinates = PointField(geography=True, unique=True)

    class Meta:
        ordering = ('address',)


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']


class Organization(models.Model):
    name = models.CharField(max_length=50)
    phones = ArrayField(models.CharField(max_length=20))
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['building']),
        ]
