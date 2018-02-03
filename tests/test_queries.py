import graphene

from . import models, types
from .testcases import GraphQLPlaceTestCase


class QueriesTests(GraphQLPlaceTestCase):

    class Query(graphene.ObjectType):
        places = graphene.List(types.PlaceType)

        def resolve_places(self, info, **kwargs):
            return models.Place.objects.all()

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
            bbox
            properties {
              name
            }
          }
        }'''

        response = self.client.execute(query)
        data = response.data['places'][0]

        self.assertGeoJSON(self.place.location, data)
        self.assertEqual(str(self.place.pk), data['id'])
        self.assertEqual(self.place.name, data['properties']['name'])
