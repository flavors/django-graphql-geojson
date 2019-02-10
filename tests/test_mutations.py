from django.contrib.gis import geos

import graphene

import graphql_geojson

from . import models, types
from .testcases import SchemaTestCase


class CreatePlace(graphene.Mutation):
    place = graphene.Field(types.PlaceType)

    class Arguments:
        name = graphene.String(required=True)
        location = graphql_geojson.Geometry(required=True)

    @classmethod
    def mutate(cls, root, info, **args):
        place = models.Place.objects.create(**args)
        return cls(place=place)


class MutationsTests(SchemaTestCase):
    query = '''
    mutation CreatePlace($name: String!, $location: Geometry!) {
      createPlace(name: $name, location: $location) {
        place {
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
    }'''

    class Mutations(graphene.ObjectType):
        create_place = CreatePlace.Field()

    def test_create_place(self):
        geometry = geos.Point(1, 0)
        response = self.execute({
            'name': 'test',
            'location': str(geometry),
        })

        data = response.data['createPlace']['place']

        self.assertGeoJSON(geometry, data)
        self.assertEqual('test', data['properties']['name'])
