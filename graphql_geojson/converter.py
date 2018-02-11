from django.contrib.gis import forms
from django.contrib.gis.db import models

import graphene
from graphene_django.converter import convert_django_field
from graphene_django.form_converter import convert_form_field

from . import fields, types


@convert_django_field.register(models.GeometryField)
def convert_field_to_geometry(field, registry=None):
    return graphene.Field(
        types.GeometryObjectType,
        description=field.help_text,
        required=not field.null)


@convert_form_field.register(forms.GeometryField)
def convert_form_field_to_geometry(field):
    return types.Geometry(
        description=field.help_text,
        required=field.required)


@convert_form_field.register(fields.DistanceField)
def convert_form_field_to_distance(field):
    return types.Distance(
        description=field.help_text,
        required=field.required)
