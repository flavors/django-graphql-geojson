import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import to_global_id

from . import nodes
from ..testcases import GraphQLPlaceTestCase


class QueriesTests(GraphQLPlaceTestCase):

    class Query(graphene.ObjectType):
        places = DjangoFilterConnectionField(nodes.PlaceNode)

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
        global_id = to_global_id(nodes.PlaceNode._meta.name, self.place.pk)

        self.assertGeoJSON(self.place.location, data)
        self.assertEqual(global_id, data['id'])
        self.assertEqual(self.place.name, data['properties']['name'])
