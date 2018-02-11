import json

from django.contrib.gis.geos import GEOSGeometry

import graphene
from graphene.types.generic import GenericScalar
from graphql.language import ast

from .. import resolver

__all__ = [
    'Geometry',
    'GeometryObjectType',
]


class Geometry(graphene.Scalar):

    @classmethod
    def serialize(cls, value):
        return json.loads(value.geojson)

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.StringValue):
            return cls.parse_value(node.value)
        return None

    @classmethod
    def parse_value(cls, value):
        if isinstance(value, dict):
            value = json.dumps(value)
        return GEOSGeometry(value)


class GeometryObjectType(graphene.ObjectType):
    type = graphene.String()
    coordinates = GenericScalar()

    class Meta:
        default_resolver = resolver.geometry_resolver
