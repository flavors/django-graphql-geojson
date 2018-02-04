from django.contrib.gis import geos
from django.test import TestCase

import graphql_geojson
from graphql.language import ast


class TypesTests(TestCase):

    def test_geojson_input(self):
        geometry = geos.Point(1, 0)
        geometry_type = graphql_geojson.Geometry()
        serialized = geometry_type.serialize(geometry)

        self.assertEqual(geometry.geom_type, serialized['type'])
        self.assertSequenceEqual(geometry.coords, serialized['coordinates'])

        node = ast.FloatValue(.0)
        self.assertIsNone(geometry_type.parse_literal(node))

        # WKT
        node = ast.StringValue(str(geometry))
        wkt_parsed = geometry_type.parse_literal(node)
        self.assertEqual(wkt_parsed, geometry)

        # GeoJSON
        geojson_parsed = geometry_type.parse_value(serialized)
        self.assertEqual(geojson_parsed.geojson, geometry.geojson)

        # Hex
        hex_parsed = geometry_type.parse_value(geometry.hexewkb)
        self.assertEqual(hex_parsed.geojson, geometry.geojson)
