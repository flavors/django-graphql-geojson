from django.contrib.gis import geos

import graphene
from graphene_django.filter import DjangoFilterConnectionField

from . import filters, nodes
from ..testcases import GraphQLPlaceTestCase


class FiltersTests(GraphQLPlaceTestCase):

    class Query(graphene.ObjectType):
        places = DjangoFilterConnectionField(
            nodes.PlaceNode,
            filterset_class=filters.PlaceFilter)

    def test_filter(self):
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

        line = geos.LineString((0, 0), (0, 2))
        response = self.client.execute(query, geometry=line.geojson)

        self.assertTrue(response.data['places']['edges'])
