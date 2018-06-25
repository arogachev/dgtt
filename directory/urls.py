from django.urls import path, register_converter

from . import converters, views

register_converter(converters.PointConverter, 'point')

urlpatterns = [
    path('organizations/by-building/<int:building_id>/', views.organizations_by_building),
    path('organizations/by-category/<int:category_id>/', views.organizations_by_category),
    path('organizations/by-radius/<point:point>/<int:radius>/', views.organizations_by_radius),
    path('organizations/by-rectangle/<point:north_west>/<point:south_east>/', views.organizations_by_rectangle),
]
