from graphql_geojson.filters import GeometryFilterSet

from .. import models


class PlaceFilter(GeometryFilterSet):

    class Meta:
        model = models.Place
        fields = {
            'name': ['exact'],
            'location': ['exact', 'intersects', 'distance_lte'],
        }
