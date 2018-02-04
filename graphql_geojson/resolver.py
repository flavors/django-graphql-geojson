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
        return list(getattr(root, default_value).extent)
    return root
