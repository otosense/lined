from functools import partial
from operator import methodcaller, itemgetter
from lined import Line
from lined.tools import map_star, iterize

transposer = map_star(zip)
transposer.__name__ = 'transposer'


def mk_transposer_to_array(dtype=None):
    """Make a transposer that transposes an iterable of n iterables of size k into an iterable of k arrays of size n.

    >>> from numpy import array
    >>> transpose = mk_transposer_to_array(dtype=int)
    >>> transpose(iter([range(1,4), range(4, 7)]))
    array([[1, 4],
           [2, 5],
           [3, 6]])
    """
    from numpy import array
    return Line(map_star(zip),
                list,
                partial(array, dtype=dtype),
                pipeline_name='transpose_to_array'
                )


mk_mapping_extractor = Line(
    iterize(itemgetter),
    lambda funcs: lambda obj: list(map(methodcaller('__call__', obj), funcs)))
mk_mapping_extractor.__module__ = __name__  # to make it seem it comes from this module (but doctests still don't work)
mk_mapping_extractor.__doc__ = """
Make a function that will extract specific fields from a mapping (e.g. dict)
    
    >>> extract_url_and_token = mk_mapping_extractor(['url', 'token'])
    >>> extract_url_and_token({'url': 'http://localhost:8888/', 'token': 42, 'another': 'field'})
    ['http://localhost:8888/', 44]
"""
