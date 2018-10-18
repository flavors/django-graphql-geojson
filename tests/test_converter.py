from django.contrib.gis.db import models
from django.test import TestCase

from graphene_django.converter import convert_django_field

from graphql_geojson import types


class FieldToGeometryTests(TestCase):

    def test_convert_geometry(self):
        field = models.PointField()
        graphene_type = convert_django_field(field)

        self.assertEqual(graphene_type.type.of_type, types.GeometryObjectType)
