from collections import namedtuple
from json import dump, dumps, loads
from os.path import isfile


def __create_object(name, kv_pairs, index=0):
    """Creates class dynamically"""
    obj = type(name, (object,), {})() # Create object of new class
    for key, value in kv_pairs:
        if isinstance(value, tuple):  # Create sub object if value is a tuple
            index += 1  # Increment index of sub objects
            value = __create_object("JsonLoadSub" + str(index), [tuple(e) for e in value._asdict().items()], index=index)
        setattr(obj, key, value)
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


def load(file_name):
    """Loads object from json"""
    if not isfile(file_name):
        raise Exception("{0} does not exist".format(file_name))

    with open(file_name) as data_file:
        data = data_file.read()

    return decode(data)


def decode(data):
    """Converts json to object"""
    tuples = loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    try:  # Try to parse tuple for key, value pairs
        if isinstance(tuples, list):  # Create list of objects
            kv_pairs = [[tuple(e) for e in tuple_._asdict().items()] for tuple_ in tuples]
            return [__create_object("JsonLoad", e) for e in kv_pairs]
        else:  # Create single object
            kv_pairs = [tuple(e) for e in tuples._asdict().items()]
            return __create_object("JsonLoad", kv_pairs)
    except:  # Return namedtuple if it fails
        return tuples


def encode(obj, indent=4):
    """Converts object to json"""
    if isinstance(obj, list):  # Convert list of objects
        return dumps([__dict(e) for e in obj], indent=indent) if indent != 0 else dumps([__dict(e) for e in obj])
    else:  # Convert single object
        return dumps(__dict(obj), indent=indent) if indent != 0 else dumps(__dict(obj))


def save(file_name, data, indent=4):
    """Saves object as json"""
    with open(file_name, "w") as outfile:
        try:  # Try to save objects
            outfile.write(encode(data, indent=indent))
        except:  # Save simple list if it fails
            dump(data, outfile, indent=indent) if indent != 0 else dump(data, outfile)
