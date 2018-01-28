import json

from django.contrib.gis.db.models import GeometryField

import graphene
from graphene.types.generic import GenericScalar
from graphene_django.converter import convert_django_field


def geojson_resolver(attname, default_value, root, info, **args):
    if default_value is not None:
        root = root or default_value
    return json.loads(root.geojson)[attname]


class GeoJSON(graphene.ObjectType):
    type = graphene.String()
    coordinates = GenericScalar()

    class Meta:
        default_resolver = geojson_resolver


@convert_django_field.register(GeometryField)
def convert_field_to_geojson(field, registry=None):
    return graphene.Field(
        GeoJSON,
        description=field.help_text,
        required=not field.null)
