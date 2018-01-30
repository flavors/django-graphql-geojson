from graphene import relay

from graphql_geojson.types import GeoJSONType

from .. import models


class PlaceNode(GeoJSONType):

    class Meta:
        model = models.Place
        interfaces = [relay.Node]
        geojson_field = 'location'
        filter_fields = ['name']
