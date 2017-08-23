from json import dump, dumps, loads
from os.path import isfile
from types import SimpleNamespace


def __object(namespace, target):
    """Converts namespace into target object"""
    obj = target()
    for attr in namespace.__dict__:
        value = getattr(namespace, attr)
        if isinstance(value, SimpleNamespace):  # Create nested object
            value = __object(value, type(getattr(obj, attr)))
        setattr(obj, attr, value)
    return obj


def __dict(obj):
    """Converts object into dictionary"""
    if not hasattr(obj, "__dict__"):
        return obj
    result = {}
    for key, value in obj.__dict__.items():
        if key.startswith("_"):
            continue
        element = []
        if isinstance(value, list):
            for item in value:
                element.append(__dict(item))
        else:
            element = __dict(value)
        result[key] = element
    return result


def decode(data, target=None):
    """Converts json into object"""
    namespaces = loads(data, object_hook=lambda d: SimpleNamespace(**d))
    if not target:  # Return namespaces
        return namespaces
    try:  # Convert namespace into object of target class, takes around 3x the time
        if isinstance(namespaces, list):  # Create list of objects
            return [__object(namespace, target) for namespace in namespaces]
        else:  # Create single object
            return __object(namespaces, target)
    except:  # Return namespaces if converting fails
        return namespaces


def load(file_name, target=None):
    """Loads object from json"""
    if not isfile(file_name):
        raise Exception("{0} does not exist".format(file_name))
    with open(file_name) as data:
        return decode(data.read(), target=target)


def encode(obj, indent=4):
    """Converts object into json"""
    if isinstance(obj, list):  # Convert list of objects
        return dumps([__dict(e) for e in obj], indent=indent) if indent != 0 else dumps([__dict(e) for e in obj])
    else:  # Convert single object
        return dumps(__dict(obj), indent=indent) if indent != 0 else dumps(__dict(obj))


def save(file_name, obj, indent=4):
    """Saves object as json"""
    with open(file_name, "w") as json:
        try:  # Try to save object
            json.write(encode(obj, indent=indent))
        except:  # Save primitive type if it fails
            dump(obj, json, indent=indent) if indent != 0 else dump(obj, json)
