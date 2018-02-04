import django_filters

from graphql_geojson.filters import GeometryFilterSet

from .. import models


class PlaceFilter(GeometryFilterSet):
    location__test = django_filters.BooleanFilter()

    class Meta:
        model = models.Place
        fields = {
            'name': ['exact'],
            'location': ['exact', 'intersects'],
        }
