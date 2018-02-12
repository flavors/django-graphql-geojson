import graphql_geojson

from .. import models


class PlaceType(graphql_geojson.GeoJSONType):

    class Meta:
        model = models.Place
        geojson_field = 'location'
