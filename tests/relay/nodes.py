import graphql_geojson
from graphene import relay

from .. import models


class PlaceNode(graphql_geojson.GeoJSONType):

    class Meta:
        model = models.Place
        interfaces = [relay.Node]
        geojson_field = 'location'
