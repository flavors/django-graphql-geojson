from django.contrib.gis.measure import D

import graphene

from .geometry import Geometry

__all__ = ['Distance']


DistanceUnitEnum = graphene.Enum('DistanceUnitEnum', [
    (value, value) for value in D.UNITS.keys()
])


class Distance(graphene.InputObjectType):
    unit = DistanceUnitEnum(required=True)
    value = graphene.Float(required=True)
    geometry = Geometry(required=True)

    class Meta:
        description = """
Distance object type comprising:
- The desired `unit` attribute name
- Distance `value`
- A `geometry` to base calculations from
"""
