def remap(value, min1, max1, min2, max2):
    """
    Remaps a value from one range to another.
    
    :param value: value to process
    :param min1: minimum value of first range
    :param max1: maximum value of first range
    :param min2: minimum value of second range
    :param max2: maximum value of second range
    :returns: remapped value
    """
    return (value - min1) / (max1 - min1) * (max2 - min2) + min2
    
    
def _sized(lst, n):
    """
    Splits a list into n-sized chunks.
    
    :param lst: list to process
    :param n: size of chunks
    :returns: generator of chunks
    """
    return (lst[i:i + n] for i in range(0, len(lst), n))

	
def sized(lst, n):
	"""
    Splits a list into n-sized chunks.
    
    :param lst: list to process
    :param n: size of chunks
    :returns: list of chunks
    """
	return list(_sized(lst, n))
    
    
def _chunk(lst, n):
    """
    Splits a list into n equally sized chunks.
    
    :param lst: list to process
    :param n: amount of chunks
    :returns: generator of chunks
    """
    quo, rem = divmod(len(lst), n)
    idc = [quo * i + min(i, rem) for i in range(n + 1)]
    return (lst[idc[i]:idc[i + 1]] for i in range(n))
    
    
def chunk(lst, n):
    """
    Splits a list into n equally sized chunks.
    
    :param lst: list to process
    :param n: amount of chunks
    :returns: list of chunks
    """
    return list(_chunk(lst, n))
    
    
def _unique(lst, key=None):
    """
    Removes duplicates from a list.
    
    :param lst: list to process
    :param key: key to apply
    :returns: generator without duplicates
    """
    seen = set()
    if key is None:
        for x in lst:
            if x not in seen:
                seen.add(x)
                yield x
    else:
        for x in lst:
            value = key(x)
            if value not in seen:
                seen.add(value)
                yield x
    
    
def unique(lst, key=None):
    """
    Removes duplicates from a list.
    
    :param lst: list to process
    :param key: key to apply
    :returs: list without duplicates
    """
    return list(_unique(lst, key=key))
    
    
def _duplicates(lst, key=None):
    """
    Finds duplicates in a list.
    
    :param lst: list to process
    :param key: key to apply
    :returns: generator of duplicates
    """
    seen = set()
    yielded = set()
    if key is None:
        for x in lst:
            if x in seen and x not in yielded:
                yielded.add(x)
                yield x
            else:
                seen.add(x)
    else:
        for x in lst:
            value = key(x)
            if value in seen and value not in yielded:
                yielded.add(value)
                yield x
            else:
                seen.add(value)
    
    
def duplicates(lst, key=None):
    """
    Finds duplicates in a list.
    
    :param lst: list to process
    :param key: key to apply
    :returns: list of duplicates
    """
    return list(_duplicates(lst, key=key))
    
    
def _compact(lst):
    """
    Removes all falsey values.
    
    :param lst: list to process
    :returns: generator without falsey values
    """
    return (x for x in lst if x)
    
    
def compact(lst):
    """
    Removes all falsey values.
    
    :param lst: list to process
    :returns: list without falsey values
    """
    return list(_compact(lst))
    
    
def index(lst, value, key=None):
    """
    Finds first index of value in a list.
    
    :param lst: list to process
    :param value: value to search
    :param key: key to apply
    :returns: first index of value
    """
    if key is not None:
        value = key(value)
    try:
        return lst.index(value)
    except ValueError:
        return -1
        
        
def _indices(lst, value, key=None):
    """
    Finds all indices of value in a list.
    
    :param lst: list to process
    :param value: value to search
    :param key: key to apply
    :returns: generator of indices
    """
    if key is not None:
        value = key(value)
    return (idx for idx, x in enumerate(lst) if x == value)
        
        
def indices(lst, value, key=None):
    """
    Finds all indices of value in a list.
    
    :param lst: list to process
    :param value: value to search
    :param key: key to apply
    :returns: list of indices
    """
    return list(_indices(lst, value, key=key))
    
    
def _flatten(lst):
    """
    Flattens a list.
    
    :param lst: list to process
    :returns: flattened generator
    """
    for x in lst:
        if isinstance(x, (list, tuple)):
            yield from _flatten(x)
        else:
            yield x

    
def flatten(lst):
    """
    Flattens a list.
    
    :param lst: list to process
    :returns: flattened list
    """
    return list(_flatten(lst))
    
    
def _concat(lst, *others):
    """
    Concatenates lists.
    
    :param lst: list to process
    :param others: lists to concatenate
    :returns: generator of concatenated lists
    """
    for x in lst:
        yield x
    for other in others:
        for x in other:
            yield x
            
            
def concat(lst, *others):
    """
    Concatenates lists.
    
    :param lst: list to process
    :param others: lists to concatenate
    :returns: list of concatenated lists
    """
    new = lst[:]
    for other in others:
        new.extend(other)
    return new
    
    
def _apply(lst, key):
    """
    Applies a key to a list.
    
    :param lst: list to process
    :param key: key to apply
    :returns: generator with applied key
    """
    return (key(x) for x in lst)
        
        
def apply(lst, key):
    """
    Applies a key to a list.
    
    :param lst: list to process
    :param key: key to apply
    :returns: list with applied key
    """
    return list(_apply(lst, key))

    
def _union(lst, *others, key=None):
    """
    Creates the union of passed lists.
    
    :param lst: list to process
    :param others: lists to unionize with
    :param key: key to apply
    :returns: unionized generator
    """
    return _unique(_concat(lst, *others), key=key)
    
    
def union(lst, *others, key=None):
    """
    Creates the union of passed lists.
    
    :param lst: list to process
    :param others: lists to unionize with
    :param key: key to apply
    :returns: unionized list
    """
    return list(_union(lst, *others, key=key))
    
    
def _difference(lst, *others, key=None):
    """
    Creates the difference of passed lists.
    
    :param lst: list to process
    :param others: lists to create difference with
    :param key: key to apply
    :returns: generator of differences
    """
    if key is None:
        seen = set(lst)
        for x in _concat(*others):
            if x not in seen:
                yield x
    else:
        seen = set(_apply(lst, key))
        for x in _concat(*others):
            if key(x) not in seen:
                yield x
    
    
def difference(lst, *others, key=None):
    """
    Creates the difference of passed lists.
    
    :param lst: list to process
    :param others: lists to create difference with
    :param key: key to apply
    :returns: list of differences
    """    
    return list(_difference(lst, *others, key=key))
    
    
def _without(lst, *values, key=None):
    """
    Creates list without values.
    
    :param lst: list to process
    :param values: values to remove
    :param key: key to apply
    :returns: generator without values
    """
    if key is None:
        values = set(values)
    else:
        values = set(_apply(values, key))
    return (x for x in lst if x not in values)
    
    
def without(lst, *values, key=None):
    """
    Creates list without values.
    
    :param lst: list to process
    :param values: values to remove
    :param key: key to apply
    :returns: list without values
    """
    return list(_without(lst, *values, key=key))
    
    
def first(lst, key):
    """
    Finds first item which evaluates key to true.
    
    :param lst: list to process
    :param key: key to evaluate
    :returns: first item which evaluates key to true.
    """
    for x in lst:
        if key(x):
            return x

    
def _where(lst, key):
    """
    Finds all items which evaluate key to true.
    
    :param lst: list to process
    :param key: key to evaluate
    :returns: generator of items evaluated to true
    """  
    return (x for x in lst if key(x))

    
def where(lst, key):
    """
    Finds all items which evaluate key to true.
    
    :param lst: list to process
    :param key: key to evaluate
    :returns: list of items evaluated to true
    """
    return list(_where(lst, key))
