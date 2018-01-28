import graphene

from . import schema
from .testcases import GraphQLTestCase


class QueriesTests(GraphQLTestCase):

    class Query(schema.ResolveMixin, graphene.ObjectType):
        places = graphene.List(schema.PlaceType)

    def test_places(self):
        query = '''
        {
          places {
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
        }'''

        response = self.client.execute(query)
        data = response.data['places'][0]

        self.assertGeoJSON(self.place.location, data)
        self.assertEqual(self.place.name, data['properties']['name'])
