import json

from django.contrib.gis.db.models import GeometryField

import graphene
from graphene.types.generic import GenericScalar
from graphene_django.converter import convert_django_field


def geometry_resolver(attname, default_value, root, info, **args):
    if default_value is not None:
        root = root or default_value
    return json.loads(root.geojson)[attname]


class Geometry(graphene.ObjectType):
    type = graphene.String()
    coordinates = GenericScalar()

    class Meta:
        default_resolver = geometry_resolver


@convert_django_field.register(GeometryField)
def convert_field_to_geometry(field, registry=None):
    return graphene.Field(
        Geometry,
        description=field.help_text,
        required=not field.null)
