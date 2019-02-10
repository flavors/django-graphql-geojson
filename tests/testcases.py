from django.contrib.gis import geos
from django.test import Client, RequestFactory, testcases

import graphene
from graphene_django.settings import graphene_settings

from . import models


class TestCase(testcases.TestCase):

    def setUp(self):
        self.place = models.Place.objects.create(
            name='somewhere',
            location=geos.Point(0, 1))


class SchemaRequestFactory(RequestFactory):

    def __init__(self, **defaults):
        super().__init__(**defaults)
        self._schema = graphene_settings.SCHEMA

    def schema(self, **kwargs):
        self._schema = graphene.Schema(**kwargs)

    def execute(self, query, **options):
        return self._schema.execute(query, **options)


class SchemaClient(SchemaRequestFactory, Client):

    def schema(self, **kwargs):
        self._schema = graphene.Schema(**kwargs)

    def execute(self, query, variables=None, **extra):
        return super().execute(query, variables=variables)


class SchemaTestCase(TestCase):
    client_class = SchemaClient
    Query = None
    Mutations = None

    def setUp(self):
        super().setUp()
        self.client.schema(query=self.Query, mutation=self.Mutations)

    def execute(self, variables=None):
        assert self.query, ('`query` property not specified')
        return self.client.execute(self.query, variables)

    def assertGeoJSON(self, geometry_field, data):
        self.assertEqual(data['type'], 'Feature')
        self.assertEqual(data['geometry']['type'], geometry_field.geom_type)
        self.assertSequenceEqual(data['bbox'], geometry_field.extent)

        self.assertSequenceEqual(
            data['geometry']['coordinates'],
            geometry_field.coords)
