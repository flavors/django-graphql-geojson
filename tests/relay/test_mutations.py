from django.contrib.gis import geos

import graphene

from graphql_geojson.types import GeoJSON

from . import nodes
from .. import models
from ..testcases import GraphQLTestCase


class CreatePlace(graphene.ClientIDMutation):
    place = graphene.Field(nodes.PlaceNode)

    class Input:
        name = graphene.String(required=True)
        location = GeoJSON(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info,
                               client_mutation_id=None, **input):

        place = models.Place.objects.create(**input)
        return cls(place=place)


class MutationsTests(GraphQLTestCase):

    class Mutations(graphene.ObjectType):
        create_place = CreatePlace.Field()

    def test_create_place(self):
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
              properties {
                name
              }
            }
            clientMutationId
          }
        }'''

        geometry = geos.Point(1, 0)
        response = self.client.execute(query, input={
            'name': 'test',
            'location': str(geometry),
        })

        data = response.data['createPlace']['place']

        self.assertGeoJSON(geometry, data)
        self.assertEqual('test', data['properties']['name'])
