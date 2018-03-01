import json
import os.path as path
import types


def _object(namespace, target):
    """
    Converts namespace into target object.

    :param namespace: namespace object
    :param target: target class
    :return: target
    """
    obj = target()
    for attr in namespace.__dict__:
        value = getattr(namespace, attr)
        if isinstance(value, types.SimpleNamespace):  # Create nested object
            value = _object(value, type(getattr(obj, attr)))
        setattr(obj, attr, value)
    return obj


def _dict(obj):
    """
    Converts object into dictionary.

    :param obj: object to convert
    :return: dict
    """
    if not hasattr(obj, "__dict__"):
        return obj
    result = {}
    for key, value in obj.__dict__.items():
        if key.startswith("_"):
            continue
        element = []
        if isinstance(value, list):
            for item in value:
                element.append(_dict(item))
        else:
            element = _dict(value)
        result[key] = element
    return result


def decode(data, target=None):
    """
    Converts json into object.

    :param data: json data
    :param target: target class
    :return: decoded data
    """
    namespaces = json.loads(data, object_hook=lambda d: types.SimpleNamespace(**d))
    if not target:  # Return namespaces
        return namespaces
    try:  # Convert namespace into object of target class, takes around 3x the time
        if isinstance(namespaces, list):  # Create list of objects
            return [_object(namespace, target) for namespace in namespaces]
        # Create single object
        return _object(namespaces, target)
    except Exception:  # Return namespaces if converting fails
        return namespaces


def load(file_name, target=None):
    """
    Loads object from json.

    :param file_name: file name
    :param target: target class
    :return: decoded data
    """
    if not path.isfile(file_name):
        raise Exception("{} does not exist".format(file_name))
    with open(file_name) as data:
        return decode(data.read(), target=target)


def encode(obj, indent=4):
    """
    Converts object into json.

    :param obj: object to convert
    :param indent: indentation level
    :return: json
    """
    if isinstance(obj, list):  # Convert list of objects
        if indent != 0:
            return json.dumps([_dict(e) for e in obj], indent=indent)
        return json.dumps([_dict(e) for e in obj])
    # Convert single object
    if indent != 0:
        return json.dumps(_dict(obj), indent=indent)
    return json.dumps(_dict(obj))


def save(file_name, obj, indent=4):
    """
    Saves object as json.

    :param file_name: file name
    :param obj: object to save
    :param indent: indentation level
    :return: None
    """
    with open(file_name, "w") as file:
        try:  # Try to save object
            file.write(encode(obj, indent=indent))
        except Exception:  # Save primitive type if it fails
            if indent != 0:
                return json.dump(obj, file, indent=indent)
            return json.dump(obj, file)
