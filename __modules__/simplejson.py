from collections import namedtuple
from json import dump, dumps, loads
from os.path import isfile


def __create_class(name, arg_names):
    """Creates class dynamically"""
    class BaseClass(object):
        def __init__(self):
            pass

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in arg_names:
                raise TypeError("Argument %s not valid for %s"
                    % (key, self.__class__.__name__))
            setattr(self, key, value)

    return type(name, (BaseClass,),{"__init__": __init__})


def load(file_name):
    """Loads objects from json"""
    if not isfile(file_name):
        raise Exception("{0} does not exist".format(file_name))

    with open(file_name) as data_file:
        data = data_file.read()

    return json_to_object(data)


def json_to_namedtuple(data):
    """Converts json to object-like tuple"""
    def hook(d):
        """Hook to access json data"""
        return namedtuple("X", d.keys())(*d.values())

    return loads(data, object_hook=hook)


def json_to_object(data):
    """Converts json to object"""
    # Create class dynamically
    tuples = json_to_namedtuple(data)
    try:  # Try to parse for object fields
        fields = [f for f in tuples[0]._fields] if type(tuples) == list else [f for f in tuples._fields]
    except:  # Return simple list if it fails
        return tuples
    LoadClass = __create_class("LoadClass", fields)

    # Load objects
    if type(tuples) == list:  # Load list of objects
        obj_list = list()
        for tuple_ in tuples:
            obj = LoadClass()
            for field in tuple_._fields:
                setattr(obj, field, getattr(tuple_, field))
            obj_list.append(obj)
        return obj_list
    else:  # Load single object
        obj = LoadClass()
        for field in tuples._fields:
            setattr(obj, field, getattr(tuples, field))
        return obj


def object_to_json(obj, indent=4):
    """Converts object to json"""
    if type(obj) == list:
        return dumps([e.__dict__ for e in obj], indent=indent)
    else:
        return dumps(obj.__dict__, indent=indent)


def save(file_name, data, indent=4):
    """Saves objects as json"""
    with open(file_name, "w") as outfile:
        try:  # Try to save objects
            outfile.write(object_to_json(data, indent=indent))
        except:  # Save simple list if it fails
            dump(data, outfile, indent=indent)
