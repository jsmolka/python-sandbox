from random import shuffle


def create_class(name, keys, values=None):
    """Creates object dynamically"""
    cls = type(name, (object,), {})
    for idx, key in enumerate(keys):
		value = values[idx] if values else None
        setattr(cls, key, value)
    return cls


def my_dict(obj):
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
                element.append(my_dict(item))
        else:
            element = my_dict(value)
        result[key] = element
    return result


def remap(v, l1, h1, l2, h2):
    """Re-maps a number from one range to another"""
    return float(v - l1) / (h1 - l1) * (h2 - l2) + l2


def shuffled(lst):
    """Returns shuffled list"""
    result = lst[:]
    shuffle(result)
    return result

	
def chunk_list(lst, count):
	"""Split list in equally sizes chunks"""
	return [lst[i:i + count] for i in range(0, len(lst), count)]
