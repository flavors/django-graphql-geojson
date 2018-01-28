import graphene
from graphene_django.filter import DjangoFilterConnectionField

from . import schema
from .testcases import GraphQLTestCase


class QueriesTests(GraphQLTestCase):

    class Query(schema.ResolveMixin, graphene.ObjectType):
        places = DjangoFilterConnectionField(schema.PlaceNode)

    def test_places(self):
        query = '''
        {
          places {
            edges {
              node {
                id
                type
                geometry {
                  type
                  coordinates
                }
                properties {
                  name
                }
              }
            }
          }
        }'''

        response = self.client.execute(query)
        data = response.data['places']['edges'][0]['node']

        self.assertGeoJSON(self.place.location, data)
        self.assertEqual(self.place.name, data['properties']['name'])
