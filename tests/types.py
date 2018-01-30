from graphql_geojson.types import GeoJSONType

from . import models


class PlaceType(GeoJSONType):

    class Meta:
        model = models.Place
        geojson_field = 'location'
