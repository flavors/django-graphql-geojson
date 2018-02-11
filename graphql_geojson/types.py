import json
from collections import OrderedDict

from django.contrib.gis.geos import GEOSGeometry

import graphene
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType, DjangoObjectTypeOptions
from graphql.language import ast

from . import resolver

__all__ = [
    'Geometry',
    'GeometryObjectType',
    'GeoJSONType',
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


class GeoJSONTypeOptions(DjangoObjectTypeOptions):
    geojson_field = None

    def __setattr__(self, name, value):
        if name == 'fields':
            geometry_field = value.pop(self.geojson_field, None)

            assert geometry_field is not None, (
                'Unrecognized field `{}`'.format(self.geojson_field)
            )

            geometry_field.name = 'geometry'
            bbox_field = graphene.Field(
                GenericScalar,
                default_value=self.geojson_field)

            primary_key = self.model._meta.pk.name
            primary_key_field = value.pop(primary_key, None)

            Properties = type('Properties', (graphene.ObjectType,), value)

            fields = [
                ('type', graphene.Field(graphene.String)),
                (self.geojson_field, geometry_field),
                ('bbox', bbox_field),
                ('properties', graphene.Field(Properties)),
            ]

            if primary_key_field is not None:
                fields.insert(1, (primary_key, primary_key_field))

            value = OrderedDict(fields)

        super().__setattr__(name, value)


class GeoJSONType(DjangoObjectType):

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, name=None, _meta=None,
                                    geojson_field=None, **options):

        assert geojson_field is not None, (
            '`{}` should either include a `Meta.geojson_field`'
            ' attribute.'.format(name or cls.__name__)
        )

        if _meta is None:
            _meta = GeoJSONTypeOptions(cls)
            _meta.geojson_field = geojson_field

        options.setdefault('default_resolver', resolver.feature_resolver)
        super().__init_subclass_with_meta__(name=name, _meta=_meta, **options)
