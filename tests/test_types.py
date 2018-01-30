from django.contrib.gis import geos
from django.test import TestCase

from graphql.language import ast

from graphql_geojson import types


class TypesTests(TestCase):

    def test_geojson(self):
        geometry = geos.Point(1, 0, srid=4326)
        geojson_type = types.GeoJSON()
        serialized = geojson_type.serialize(geometry)

        self.assertEqual(geometry.geom_type, serialized['type'])
        self.assertEqual(list(geometry.coords), serialized['coordinates'])

        node = ast.FloatValue(.0)
        self.assertIsNone(geojson_type.parse_literal(node))

        # WKT
        node = ast.StringValue(str(geometry))
        wkt_parsed = geojson_type.parse_literal(node)
        self.assertEqual(wkt_parsed, geometry)

        # GeoJSON
        geojson_parsed = geojson_type.parse_value(serialized)
        self.assertEqual(geojson_parsed, geometry)

        # Hex
        hex_parsed = geojson_type.parse_value(geometry.hexewkb)
        self.assertEqual(hex_parsed, geometry)
