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

    pip install django-graphql-geojson --process-dependency-links


GeoJSONType
-----------

``models.py``

.. code:: python

    from django.contrib.gis.db import models


    class Place(models.Model):
        name = models.CharField(max_length=255)
        location = models.PointField()



``schema.py``

.. code:: python

    from graphql_geojson.types import GeoJSONType


    class PlaceType(GeoJSONType):

        class Meta:
            model = models.Place
            geojson_field = 'location'


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
        properties {
          name
        }
      }
    }


GeoJSONInput
-----------

``schema.py``

.. code:: python

    import graphene

    from graphql_geojson.types import GeoJSONInput


    class CreatePlace(graphene.Mutation):
        place = graphene.Field(types.PlaceType)

        class Arguments:
            name = graphene.String(required=True)
            location = GeoJSONInput(required=True)

        @classmethod
        def mutate(cls, root, info, **args):
            place = models.Place.objects.create(**args)
            return cls(place=place)


**Mutation**

.. code:: graphql

    mutation CreatePlace($name: String!, $location: GeoJSONInput!) {
      createPlace(name: $name, location: $location) {
        place {
          id
        }
      }
    }

**GeoJSONInput** object may be initialized in a few ways:

- Well-known text (WKT):

.. code:: python

    'POINT(5 23)'

- Hexadecimal (HEX):

.. code:: python

    '010100000000000000000014400000000000003740'

- GeoJSON:

.. code:: python

    {
      "type": "Point",
      "coordinates": [
        5.000000,
        23.000000
      ]
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
