from unittest.mock import Mock

from django.contrib.gis import geos
from django.test import TestCase

from graphql_geojson import resolver

from .models import Place


class ResolverTests(TestCase):

    def test_geometry_resolver(self):
        geometry = geos.Point(0, 1)
        resolved = resolver.geometry_resolver(
            attname='type',
            default_value=None,
            root=geometry,
            info=None)

        self.assertEqual(resolved, 'Point')

    def test_geometry_default_resolver(self):
        geometry = geos.LineString((0, 0), (0, 1))
        resolved = resolver.geometry_resolver(
            attname='type',
            default_value=geometry,
            root=None,
            info=None)

        self.assertEqual(resolved, 'LineString')

    def test_feature_bbox_resolver_null_geometry(self):
        resolved = resolver.feature_resolver(
            attname='bbox',
            default_value='location',
            root=Place(),
            info=Mock())

        self.assertIsNone(resolved)
