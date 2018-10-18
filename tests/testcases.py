from django.contrib.gis import geos
from django.test import Client, RequestFactory, testcases

import graphene
from graphene.types.generic import GenericScalar

from . import models


class SchemaRequestFactory(RequestFactory):

    def execute(self, query, **variables):
        return self._schema.execute(query, variables=variables)


class SchemaClient(SchemaRequestFactory, Client):

    def __init__(self, **defaults):
        super().__init__(**defaults)
        self._schema = None

    def schema(self, **kwargs):
        self._schema = graphene.Schema(**kwargs)


class SchemaTestCase(testcases.TestCase):
    client_class = SchemaClient

    class Query(graphene.ObjectType):
        test = GenericScalar()

    Mutations = None

    def setUp(self):
        self.client.schema(query=self.Query, mutation=self.Mutations)

    def assertGeoJSON(self, geometry_field, data):
        self.assertEqual(data['type'], 'Feature')
        self.assertEqual(data['geometry']['type'], geometry_field.geom_type)
        self.assertSequenceEqual(data['bbox'], geometry_field.extent)

        self.assertSequenceEqual(
            data['geometry']['coordinates'],
            geometry_field.coords)


class PlacesSchemaTestCase(SchemaTestCase):

    def setUp(self):
        super().setUp()
        self.place = models.Place.objects.create(
            name='somewhere',
            location=geos.Point(0, 1))
