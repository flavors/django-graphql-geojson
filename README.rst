Django GraphQL GeoJSON
======================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|

`GeoJSON`_ support for `Django GraphQL`_

.. _GeoJSON: http://geojson.org
.. _Django GraphQL: https://github.com/graphql-python/graphene-django


Dependencies
------------

* Python ≥ 3.4
* Django ≥ 1.11


Installation
------------

Install last stable version from Pypi.

.. code:: sh

    pip install django-graphql-geojson


GeoJSONType
-----------

``GeoJSONType`` is a subclass of ``DjangoObjectType`` which provides GraphQL fields in **GeoJSON** format.

Just define a ``Meta.geojson_field`` to be represented as a ``Geometry`` type.


**models.py**

.. code:: python

    from django.contrib.gis.db import models


    class Place(models.Model):
        name = models.CharField(max_length=255)
        location = models.PointField()


**schema.py**

.. code:: python

    import graphene
    import graphql_geojson


    class PlaceType(graphql_geojson.GeoJSONType):

        class Meta:
            model = models.Place
            geojson_field = 'location'


    class Query(graphene.ObjectType):
        places = graphene.List(PlaceType)


    schema = graphene.Schema(query=Query)


**Query**

.. code:: graphql

    query {
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
    }


Geometry Type
-------------

``Geometry`` is a special GraphQL type that represents a `GEOS geometry object`_.

.. _GEOS geometry object: https://docs.djangoproject.com/en/2.0/ref/contrib/gis/geos/#geometry-objects

**schema.py**

.. code:: python

    import graphene
    import graphql_geojson


    class CreatePlace(graphene.Mutation):
        place = graphene.Field(types.PlaceType)

        class Arguments:
            name = graphene.String(required=True)
            location = graphql_geojson.Geometry(required=True)

        @classmethod
        def mutate(cls, root, info, **args):
            place = models.Place.objects.create(**args)
            return cls(place=place)


**Mutation**

.. code:: graphql

    mutation CreatePlace($name: String!, $location: Geometry!) {
      createPlace(name: $name, location: $location) {
        place {
          id
        }
      }
    }


``Geometry`` type may be initialized in a few ways:

- Well-known text (WKT):

.. code:: python

    "POINT(5 23)"

- Hexadecimal (HEX):

.. code:: python

    "010100000000000000000014400000000000003740"

- GeoJSON:

.. code:: python

    {
      "type": "Point",
      "coordinates": [5, 23]
    }


GeometryFilterSet
-----------------

Django GraphQL GeoJSON provides a custom FilterSet for `spatial lookups`_.

.. _spatial lookups: https://docs.djangoproject.com/en/2.0/ref/contrib/gis/geoquerysets/#spatial-lookups

The ``Meta.fields`` option is combined with model to automatically generate filters. 

**filters.py**

.. code:: python

    from graphql_geojson.filters import GeometryFilterSet


    class PlaceFilter(GeometryFilterSet):

        class Meta:
            model = models.Place
            fields = {
                'name': ['exact'],
                'location': ['exact', 'intersects', 'distance_lte'],
            }


**schema.py**

.. code:: python

    import graphene
    import graphql_geojson
    from graphene import relay
    from graphene_django.filter import DjangoFilterConnectionField


    class PlaceNode(graphql_geojson.GeoJSONType):

        class Meta:
            model = Place
            interfaces = [relay.Node]
            geojson_field = 'location'


    class Query(graphene.ObjectType):
        places = DjangoFilterConnectionField(
            PlaceNode,
            filterset_class=PlaceFilter)


**Query**

.. code:: graphql

      query Places($geometry: Geometry!){
        places(location_Intersects: $geometry) {
          edges {
            node {
              id
            }
          }
        }
      }


`Distance lookups`_ take a ``Distance`` parameter comprising:

- The desired `unit attribute`_ name 
- Distance value
- A geometry to base calculations from

.. _Distance lookups: https://docs.djangoproject.com/en/2.0/ref/contrib/gis/db-api/#distance-lookups
.. _unit attribute: https://docs.djangoproject.com/en/2.0/ref/contrib/gis/measure/#supported-units

.. code:: graphql

      query Places(
          $unit: DistanceUnitEnum!,
          $value: Float!,
          $geometry: Geometry!)
        {
        places(location_DistanceLte: {
            unit: $unit,
            value: $value,
            geometry: $geometry
          }) {
          edges {
            node {
              id
            }
          }
        }
      }

----

.. raw:: html

    <embed>
    <p align="center">
       If you have a <strong>problem</strong> don't hesitate to <a href="https://github.com/flavors/django-graphql-geojson/issues/new">ask for assistance</a>.
       <br>
       <a href="https://github.com/flavors/django-graphql-geojson/issues/new"><img src="https://user-images.githubusercontent.com/5514990/35416955-36d33b32-0251-11e8-9dd8-4b8c92adae68.gif"></a>
    </p>
    </embed>


.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphql-geojson.svg
   :target: https://pypi.python.org/pypi/django-graphql-geojson

.. |Wheel| image:: https://img.shields.io/pypi/wheel/django-graphql-geojson.svg
   :target: https://pypi.python.org/pypi/django-graphql-geojson

.. |Build Status| image:: https://travis-ci.org/flavors/django-graphql-geojson.svg?branch=master
   :target: https://travis-ci.org/flavors/django-graphql-geojson

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/django-graphql-geojson.svg
   :target: https://codecov.io/gh/flavors/django-graphql-geojson

.. |Code Climate| image:: https://api.codeclimate.com/v1/badges/67dbb917ad4cf8c422a6/maintainability
   :target: https://codeclimate.com/github/flavors/django-graphql-geojson
