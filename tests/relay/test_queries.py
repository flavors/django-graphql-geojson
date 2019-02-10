import graphene
from graphene_django.fields import DjangoConnectionField
from graphql_relay import to_global_id

from . import nodes
from ..testcases import SchemaTestCase


class QueriesTests(SchemaTestCase):
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
            bbox
            properties {
              name
            }
          }
        }
      }
    }'''

    class Query(graphene.ObjectType):
        places = DjangoConnectionField(nodes.PlaceNode)

    def test_places(self):
        response = self.execute()
        data = response.data['places']['edges'][0]['node']
        global_id = to_global_id(nodes.PlaceNode._meta.name, self.place.pk)

        self.assertGeoJSON(self.place.location, data)
        self.assertEqual(global_id, data['id'])
        self.assertEqual(self.place.name, data['properties']['name'])
