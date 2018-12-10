def remap(x, x1, x2, y1, y2):
    """
    Remaps a value from one range to another.

    :param x: value to process
    :param x1, x2: range of x
    :param y1, y2: new range
    :return: float
    """
    return (x - x1) / (x2 - x1) * (y2 - y1) + y1


def sized_gen(lst, n):
    """
    Splits a list into n-sized chunks.

    :param lst: list to process
    :param n: size of chunks
    :return: generator
    """
    n = min(max(1, n), len(lst))
    for idx in range(0, len(lst), n):
        yield lst[idx:idx + n]


def sized(lst, n):
    """
    Splits a list into n-sized chunks.

    :param lst: list to process
    :param n: size of chunks
    :return: list
    """
    return list(sized_gen(lst, n))


def chunk_gen(lst, n):
    """
    Splits a list into n equally sized chunks.

    :param lst: list to process
    :param n: amount of chunks
    :return: generator
    """
    n = min(max(1, n), len(lst))
    quo, rem = divmod(len(lst), n)
    idc = [quo * idx + min(idx, rem) for idx in range(n + 1)]
    for idx in range(n):
        yield lst[idc[idx]:idc[idx + 1]]


def chunk(lst, n):
    """
    Splits a list into n equally sized chunks.

    :param lst: list to process
    :param n: amount of chunks
    :return: list
    """
    return list(chunk_gen(lst, n))


def unique_gen(lst, key=None):
    """
    Removes duplicates from a list.

    :param lst: list to process
    :param key: key to apply
    :return: generator
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
    :return: list
    """
    return list(unique_gen(lst, key=key))


def duplicates_gen(lst, key=None):
    """
    Finds duplicates in a list.

    :param lst: list to process
    :param key: key to apply
    :return: generator
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
    :return: list
    """
    return list(duplicates_gen(lst, key=key))


def compact_gen(lst, key=None):
    """
    Removes all falsy values.

    :param lst: list to process
    :param key: key to apply
    :return: generator
    """
    if key is None:
        for x in lst:
            if x:
                yield x
    else:
        for x in lst:
            if key(x):
                yield x


def compact(lst, key=None):
    """
    Removes all falsy values.

    :param lst: list to process
    :param key: key to apply
    :return: list
    """
    return list(compact_gen(lst, key=key))


def index(lst, value, key=None):
    """
    Finds first index of value in a list.

    :param lst: list to process
    :param value: value to search
    :param key: key to apply
    :return: int
    """
    if key is not None:
        value = key(value)
    try:
        return lst.index(value)
    except ValueError:
        return -1


def apply_gen(lst, key):
    """
    Applies a key to a list.

    :param lst: list to process
    :param key: key to apply
    :return: map
    """
    return map(key, lst)


def apply(lst, key):
    """
    Applies a key to a list.

    :param lst: list to process
    :param key: key to apply
    :return: list
    """
    return list(apply_gen(lst, key))


def indices_gen(lst, *values, key=None):
    """
    Finds all indices of value in a list.

    :param lst: list to process
    :param values: values to search
    :param key: key to apply
    :return: generator
    """
    values = set(values)
    if key is None:
        for idx, x in enumerate(lst):
            if x in values:
                yield idx
    else:
        for idx, x in enumerate(lst):
            if key(x) in values:
                yield idx


def indices(lst, *values, key=None):
    """
    Finds all indices of value in a list.

    :param lst: list to process
    :param values: values to search
    :param key: key to apply
    :return: list
    """
    return list(indices_gen(lst, *values, key=key))


def flatten_gen(lst):
    """
    Flattens a list.

    :param lst: list to process
    :return: generator
    """
    for x in lst:
        if isinstance(x, list):
            yield from flatten_gen(x)
        else:
            yield x


def flatten(lst):
    """
    Flattens a list.

    :param lst: list to process
    :return: list
    """
    return list(flatten_gen(lst))


def concat_gen(lst, *others):
    """
    Concatenates lists.

    :param lst: list to process
    :param others: lists to concatenate
    :return: generator
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
    :return: list
    """
    new = lst[:]
    for other in others:
        new.extend(other)
    return new


def union_gen(lst, *others, key=None):
    """
    Creates the union of passed lists.

    :param lst: list to process
    :param others: lists to unionize with
    :param key: key to apply
    :return: generator
    """
    return unique_gen(concat_gen(lst, *others), key=key)


def union(lst, *others, key=None):
    """
    Creates the union of passed lists.

    :param lst: list to process
    :param others: lists to unionize with
    :param key: key to apply
    :return: list
    """
    return list(union_gen(lst, *others, key=key))


def difference_gen(lst, other, key=None):
    """
    Creates the difference of passed lists.

    :param lst: list to process
    :param other: list to create difference with
    :param key: key to apply
    :return: generator
    """
    if key is None:
        seen = set(other)
        for x in lst:
            if x not in seen:
                yield x
    else:
        seen = set(apply_gen(other, key))
        for x in lst:
            if key(x) not in seen:
                yield x


def difference(lst, other, key=None):
    """
    Creates the difference of passed lists.

    :param lst: list to process
    :param other: lists to create difference with
    :param key: key to apply
    :return: list
    """
    return list(difference_gen(lst, other, key=key))


def without_gen(lst, *values, key=None):
    """
    Creates list without values.

    :param lst: list to process
    :param values: values to remove
    :param key: key to apply
    :return: generator
    """
    values = set(values)
    if key is None:
        for x in lst:
            if x not in values:
                yield x
    else:
        for x in lst:
            if key(x) not in values:
                yield x


def without(lst, *values, key=None):
    """
    Creates list without values.

    :param lst: list to process
    :param values: values to remove
    :param key: key to apply
    :return: list
    """
    return list(without_gen(lst, *values, key=key))


def first(lst, key):
    """
    Finds first item which evaluates key to true.

    :param lst: list to process
    :param key: key to evaluate
    :return: item
    """
    for x in lst:
        if key(x):
            return x


def where_gen(lst, key):
    """
    Finds all items which evaluate key to true.

    :param lst: list to process
    :param key: key to evaluate
    :return: generator
    """
    for x in lst:
        if key(x):
            yield x


def where(lst, key):
    """
    Finds all items which evaluate key to true.

    :param lst: list to process
    :param key: key to evaluate
    :return: list
    """
    return list(where_gen(lst, key))


def powerset_gen(lst):
    """
    Calculates the powerset.

    :param lst: list to process
    :return: generator
    """
    if lst:
        for x in powerset(lst[1:]):
            yield x + [lst[0]]
            yield x
    else:
        yield []


def powerset(lst):
    """
    Calculates the powerset.

    :param lst: list to process
    :return: list
    """
    return list(powerset_gen(lst))


def mask_gen(lst, *values, key=None):
    """
    Creates a bool mask.

    :param lst: list to process
    :param values: values to mask
    :param key: key to apply
    :return: generator
    """
    values = set(values)
    if key is None:
        for x in lst:
            yield x in values
    else:
        for x in lst:
            yield key(x) in values


def mask(lst, *values, key=None):
    """
    Creates a bool mask.

    :param lst: list to process
    :param values: values to mask
    :param key: key to apply
    :return: list
    """
    return list(mask_gen(lst, *values, key=key))


def invert_gen(lst, key=None):
    """
    Inverts a list.

    :param lst: list to process
    :param key: key to apply
    :return: generator
    """
    if key is None:
        for x in lst:
            yield not x
    else:
        for x in lst:
            yield not key(x)


def invert(lst, key=None):
    """
    Inverts a list.

    :param lst: list to process
    :param key: key to apply
    :return: list
    """
    return list(invert_gen(lst, key=key))
