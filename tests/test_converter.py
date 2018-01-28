from django.contrib.gis import geos
from django.contrib.gis.db import models
from django.test import TestCase

from graphene_django.converter import convert_django_field

from graphql_geojson import converter


class ConverterTests(TestCase):

    def test_geojson_resolver(self):
        geometry = geos.Point(0, 1)
        resolved = converter.geojson_resolver(
            attname='type',
            default_value=None,
            root=geometry,
            info=None)

        self.assertEqual(resolved, 'Point')

    def test_geojson_default_resolver(self):
        geometry = geos.LineString((0, 0), (0, 1))
        resolved = converter.geojson_resolver(
            attname='type',
            default_value=geometry,
            root=None,
            info=None)

        self.assertEqual(resolved, 'LineString')

    def test_convert_geometry(self):
        field = models.PointField()
        graphene_type = convert_django_field(field)
        self.assertEqual(graphene_type.type.of_type, converter.GeoJSON)
