from django.contrib.gis.measure import D

import graphene

from .geometry import Geometry

__all__ = ['Distance']


UnitEnum = graphene.Enum('UnitEnum', [
    (value, value) for value in D.UNITS.keys()
])


class Distance(graphene.InputObjectType):
    unit = UnitEnum(required=True)
    value = graphene.Float(required=True)
    geometry = Geometry(required=True)
