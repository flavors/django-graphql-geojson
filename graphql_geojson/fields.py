from django import forms
from django.contrib.gis.measure import D


class DistanceField(forms.Field):

    def to_python(self, value):
        if value in self.empty_values:
            return None
        return (value['geometry'], D(**{value['unit']: value['value']}))
