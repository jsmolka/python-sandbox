def remap(value, min1, max1, min2, max2):
    """
    Re-maps a value from one range to another.
    
    :param value: values to be remapped
    :param min1: minimum value of first range
    :param max1: maximum value of first range
    :param min2: minimum value of second range
    :param max2: maximum value of second range
    :returns: remapped value
    """
    return (value - min1) / (max1 - min1) * (max2 - min2) + min2

	
def sized(lst, n):
	"""
    Splits a list into n-sized chunks.
    
    :param lst: list to process
    :param n: size of chunks
    :returns: list of chunks
    """
	return [lst[i:i + n] for i in range(0, len(lst), n)]
    
    
def chunk(lst, n):
    """
    Splits a list into n equally sized chunks.
    
    :param lst: list to process
    :param n: amount of chunks
    :returns: list of chunks
    """
    quo, rem = divmod(len(lst), n)
    idc = [quo * i + min(i, rem) for i in range(n + 1)]
    return [lst[idc[i]:idc[i + 1]] for i in range(n)]
    
    
def _unique(lst, key):
    """
    Removes duplicates from a list.
    
    :param lst: list to process
    :param key: key for removing duplicates
    :returns: generator without duplicates
    """
    seen = set()
    for x in lst:
        val = key(x)
        if val in seen:
            continue
        seen.add(val)
        yield x
    
    
def unique(lst, key=lambda x: x):
    """
    Removes duplicates from a list.
    
    :param lst: list to process
    :param key: key for removing duplicates
    :returs: list without duplicates
    """
    return list(_unique(lst, key))
    
    
def compact(lst):
    """
    Removes all falsey values.
    
    :param lst: list to process
    :returns: list without falsey values
    """
    return [x for x in lst if x]
    
    
def index(lst, value):
    """
    Finds first index of value in a list.
    
    :param lst: list to process
    :param value: value to be searched
    :returns: first index of value
    """
    try:
        return lst.index(value)
    except ValueError:
        return -1
        
        
def indices(lst, value):
    """
    Finds all indices of value in a list.
    
    :param lst: list to process
    :param value: value to be searched
    :returns: list of indices
    """
    return [idx for idx, x in enumerate(lst) if x == value]
    
    
def _flatten(lst):
    """
    Flattens list.
    
    :param lst: list to be flattened
    :returns: generator of flattened list
    """
    for x in lst:
        try:
            yield from _flatten(x)
        except TypeError:
            yield x

    
def flatten(lst):
    """
    Flattens list.
    
    :param lst: list to be flattened
    :returns: flattened list
    """
    return list(_flatten(lst))
    
    
def union(lst, *others):
    """
    Creates union of passed lists.
    
    :param lst: list to union with
    :param others: lists to unionize with
    :returns: unionized list
    """
    return unique(flatten(lst + list(others)))
    
    
def without(lst, *values):
    """
    Creates list without values.
    
    :param lst: list to process
    :param values: values to be removed
    :returns: list without values
    """
    values = set(values)
    return [x for x in lst if x not in values]
    
    
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

    
def where(lst, key):
    """
    Finds all items which evaluate key to true.
    
    :param lst: list to process
    :param key: key to evaluate
    :returns: list of items which evaluate key to true
    """    
    return [x for x in lst if key(x)]
    
    
def times(n, func):
    """
    Returns list with n-times the function result.
    
    :param n: number of repeats
    :param func: function called for each iteration
    :returns: list of n-times the function result
    """
    return [func() for i in range(n)]
