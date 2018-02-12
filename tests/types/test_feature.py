from django.test import TestCase

from graphql_geojson.types import feature as types


class FeatureTypeTests(TestCase):

    def test_ordered_fields(self):
        ordered_fields = types.OrderedFields()
        ordered_fields.update(test=True)

        self.assertTrue(ordered_fields['test'])
