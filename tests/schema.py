from graphene import relay

from graphql_geojson.types import GeoJSONType

from . import models


class PlaceType(GeoJSONType):

    class Meta:
        model = models.Place
        geojson_field = 'location'


class PlaceNode(GeoJSONType):

    class Meta:
        model = models.Place
        interfaces = [relay.Node]
        geojson_field = 'location'
        filter_fields = ['name']


class ResolveMixin(object):

    def resolve_places(self, info, **kwargs):
        return models.Place.objects.all()
