from collections import OrderedDict

import graphene
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType, DjangoObjectTypeOptions

from .. import resolver

__all__ = ['GeoJSONType']


class OrderedFields(OrderedDict):

    def update(self, other=None, **kwargs):
        if other is not None:
            global_id_field = other.pop('id', None)

            if global_id_field is not None:
                self['id'] = global_id_field

            properties_type = self['properties']._type
            Properties = type(properties_type.__name__, (
                properties_type,), other)

            self['properties'] = graphene.Field(Properties)
        else:
            super().update(**kwargs)


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

            value.update({
                key: attr for key, attr in self.class_type.__dict__.items()
                if key.startswith('resolve') and callable(attr)
            })

            Properties = type('{}Properties'.format(self.model.__name__), (
                graphene.ObjectType,), value)

            fields = [
                ('type', graphene.Field(graphene.String)),
                (self.geojson_field, geometry_field),
                ('bbox', bbox_field),
                ('properties', graphene.Field(Properties)),
            ]

            if primary_key_field is not None:
                fields.insert(1, (primary_key, primary_key_field))

            value = OrderedFields(fields)

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
        super().__init_subclass_with_meta__(name=name, _meta=_meta,  **options)
