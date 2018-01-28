from collections import OrderedDict

import graphene
from graphene_django.types import DjangoObjectType, DjangoObjectTypeOptions


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
