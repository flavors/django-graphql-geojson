import django_filters

from django.contrib.gis import forms
from django.contrib.gis.db import models


class GeometryFilter(django_filters.Filter):
    field_class = forms.GeometryField


FILTER_DEFAULTS = django_filters.FilterSet.FILTER_DEFAULTS
FILTER_DEFAULTS.update({
    models.GeometryField: {
        'filter_class': GeometryFilter,
    },
})


class GeometryFilterSet(django_filters.FilterSet):
    FILTER_DEFAULTS = FILTER_DEFAULTS
