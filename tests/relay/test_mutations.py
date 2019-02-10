from django.contrib.gis import geos

import graphene

import graphql_geojson

from . import nodes
from .. import models
from ..testcases import SchemaTestCase


class CreatePlace(graphene.ClientIDMutation):
    place = graphene.Field(nodes.PlaceNode)

    class Input:
        name = graphene.String(required=True)
        location = graphql_geojson.Geometry(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info,
                               client_mutation_id=None, **input):

        place = models.Place.objects.create(**input)
        return cls(place=place)


class MutationsTests(SchemaTestCase):
    query = '''
    mutation CreatePlace($input: CreatePlaceInput!) {
      createPlace(input: $input) {
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
        clientMutationId
      }
    }'''

    class Mutations(graphene.ObjectType):
        create_place = CreatePlace.Field()

    def test_create_place(self):
        geometry = geos.Point(1, 0)
        response = self.execute({
            'input': {
                'name': 'test',
                'location': str(geometry),
            },
        })

        data = response.data['createPlace']['place']

        self.assertGeoJSON(geometry, data)
        self.assertEqual('test', data['properties']['name'])
