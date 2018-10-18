from django.test import TestCase

from graphene_django.types import DjangoObjectTypeOptions

from graphql_geojson.types import feature as types

from .. import models


class OrderedFieldsTests(TestCase):

    def test_update_ordered_fields(self):
        ordered_fields = types.OrderedFields()
        ordered_fields.update(test=True)

        self.assertTrue(ordered_fields['test'])


class GeoJSONTypeTests(TestCase):

    def test_custom_meta(self):

        class GeoJSONType(types.GeoJSONType):

            class Meta:
                abstract = True

            @classmethod
            def __init_subclass_with_meta__(cls, **options):
                options.setdefault('_meta', DjangoObjectTypeOptions(cls))
                super().__init_subclass_with_meta__(**options)

        class PlaceType(GeoJSONType):

            class Meta:
                model = models.Place
                geojson_field = 'location'

        self.assertIsInstance(PlaceType._meta, DjangoObjectTypeOptions)

    def test_options_missing_pk(self):

        class PlaceType(types.GeoJSONType):

            class Meta:
                model = models.Place
                geojson_field = 'location'
                only_fields = ['location']

        self.assertNotIn('id', PlaceType()._meta.fields)
