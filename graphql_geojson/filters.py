from django.contrib.gis import forms
from django.contrib.gis.db import models

import django_filters

from . import fields


class GeometryFilter(django_filters.Filter):
    field_class = forms.GeometryField


class DistanceFilter(django_filters.Filter):
    field_class = fields.DistanceField


FILTER_DEFAULTS = django_filters.FilterSet.FILTER_DEFAULTS
FILTER_DEFAULTS.update({
    models.GeometryField: {
        'filter_class': GeometryFilter,
    },
})


class GeometryFilterSet(django_filters.FilterSet):
    FILTER_DEFAULTS = FILTER_DEFAULTS

    @classmethod
    def filter_for_lookup(cls, field, lookup_type):
        if lookup_type.startswith('distance'):
            return DistanceFilter, {}
        return super().filter_for_lookup(field, lookup_type)
