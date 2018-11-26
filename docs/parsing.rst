Parsing
=======

Parsing is the act of compiling the raw jsonmask string into a Python dictionary that represents the nested structure of the map. Consider the following examples:

`No nested data:`
    >>> from jsonmask import parse_fields
    >>> parse_fields('a,b,c')
    {
        'a': {},
        'b': {},
        'c': {},
    }

`Simple nested data:`
    >>> from jsonmask import parse_fields
    >>> parse_fields('a,b/c')
    {
        'a': {},
        'b': {
            'c': {},
        },
    }


`Nested data with multiple fields:`
    >>> from jsonmask import parse_fields
    >>> parse_fields('a,b/c,c(d,e,f)')
    {
        'a': {},
        'b': {
            'c': {},
        },
        c: {
            'd': {},
            'e': {},
            'f': {},
        },
    }


When the masker reaches a terminal value of ``{}``, it is done pruning and includes any futher nested children.
