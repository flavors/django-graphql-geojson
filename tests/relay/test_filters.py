from django.contrib.gis import geos

import graphene
from graphene_django.filter import DjangoFilterConnectionField

from . import filters, nodes
from ..testcases import SchemaTestCase


class FilterTestsCase(SchemaTestCase):

    class Query(graphene.ObjectType):
        places = DjangoFilterConnectionField(
            nodes.PlaceNode,
            filterset_class=filters.PlaceFilter)


class FilterIntersectsTests(FilterTestsCase):
    query = '''
    query Places($geometry: Geometry!) {
      places(location_Intersects: $geometry) {
        edges {
          node {
            id
          }
        }
      }
    }'''

    def test_filter_intersects(self):
        line = geos.LineString((0, 0), (0, 2), srid=4326)
        response = self.execute({'geometry': str(line)})

        self.assertTrue(response.data['places']['edges'])


class FilterDistanceTests(FilterTestsCase):
    query = '''
    query Places(
        $unit: DistanceUnitEnum!,
        $value: Float!,
        $geometry: Geometry!)
      {
      places(location_DistanceLte: {
          unit: $unit,
          value: $value,
          geometry: $geometry
        }) {
        edges {
          node {
            id
          }
        }
      }
    }'''

    def test_filter_distance(self):
        line = geos.LineString((0, 0), (1, 1), srid=4326)
        response = self.execute({
            'unit': 'km',
            'value': 100,
            'geometry': str(line),
        })

        self.assertTrue(response.data['places']['edges'])
