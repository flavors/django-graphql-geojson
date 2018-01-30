from django.contrib.gis import geos

import graphene

from graphql_geojson.types import GeoJSON

from . import models, types
from .testcases import GraphQLTestCase


class CreatePlace(graphene.Mutation):
    place = graphene.Field(types.PlaceType)

    class Arguments:
        name = graphene.String(required=True)
        location = GeoJSON(required=True)

    @classmethod
    def mutate(cls, root, info, **args):
        place = models.Place.objects.create(**args)
        return cls(place=place)


class MutationsTests(GraphQLTestCase):

    class Mutations(graphene.ObjectType):
        create_place = CreatePlace.Field()

    def test_create_place(self):
        query = '''
        mutation CreatePlace($name: String!, $location: GeoJSON!) {
          createPlace(name: $name, location: $location) {
            place {
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
        }'''

        geometry = geos.Point(1, 0)
        response = self.client.execute(
            query,
            name='test',
            location=str(geometry))

        data = response.data['createPlace']['place']

        self.assertGeoJSON(geometry, data)
        self.assertEqual('test', data['properties']['name'])
