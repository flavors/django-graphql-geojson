import json


def geometry_resolver(attname, default_value, root, info, **args):
    if default_value is not None:
        root = root or default_value
    return json.loads(root.geojson)[attname]


def feature_resolver(attname, default_value, root, info, **args):
    if attname == 'type':
        return 'Feature'

    elif info.field_name == 'geometry':
        return getattr(root, attname)

    elif attname == 'bbox':
        geometry = getattr(root, default_value)

        if geometry is not None:
            return geometry.extent
        return None

    return root
