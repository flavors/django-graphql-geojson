import json
from collections import OrderedDict

from django.contrib.gis.geos import GEOSGeometry

import graphene
from graphene_django.types import DjangoObjectType, DjangoObjectTypeOptions
from graphql.language import ast


class GeoJSONInput(graphene.Scalar):

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


class GeoJSONTypeOptions(DjangoObjectTypeOptions):
    geojson_field = None

    def __setattr__(self, name, value):
        if name == 'fields':
            geometry_field = value.pop(self.geojson_field)
            geometry_field.name = 'geometry'

            primary_key = self.model._meta.pk.name
            primary_key_field = value.pop(primary_key, None)

            Properties = type('Properties', (graphene.ObjectType,), value)

            fields = [
                ('type', graphene.Field(graphene.String)),
                (self.geojson_field, geometry_field),
                ('properties', graphene.Field(Properties)),
            ]

            if primary_key_field is not None:
                fields.insert(0, ('id', primary_key_field))

            value = OrderedDict(fields)

        super().__setattr__(name, value)


def feature_resolver(attname, default_value, root, info, **args):
    if attname == 'type':
        return 'Feature'
    elif info.field_name == 'geometry':
        return getattr(root, attname)
    return root


class GeoJSONType(DjangoObjectType):

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, name=None, geojson_field=None,
                                    default_resolver=None, **options):

        assert geojson_field is not None, (
            '`{}` should either include a `Meta.geojson_field`'
            ' attribute.'.format(name or cls.__name__)
        )

        _meta = GeoJSONTypeOptions(cls)
        _meta.geojson_field = geojson_field

        super().__init_subclass_with_meta__(
            default_resolver=feature_resolver,
            name=name, _meta=_meta, **options)
