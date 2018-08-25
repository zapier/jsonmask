"""Sample unit test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison
import logging

from expecter import expect

from jsonmask import parsing


def test_multiple_builds():
    tests = [
        {
            'fields': 'a,b',
            'mask': {'a': {}, 'b': {}},
        },
        {
            'fields': 'a/b',
            'mask': {'a': {'b': {}}},
        },
        {
            'fields': 'a/b,c',
            'mask': {'a': {'b': {}}, 'c': {}},
        },
        {
            'fields': 'a/b,a/c',
            'mask': {'a': {'b': {}, 'c': {}}},
        },
        {
            'fields': 'a/b,a/c,c',
            'mask': {'a': {'b': {}, 'c': {}}, 'c': {}},
        },
        {
            'fields': 'a/b/z,a/c,c',
            'mask': {'a': {'b': {'z': {}}, 'c': {}}, 'c': {}},
        },
        {
            'fields': 'a(b)',
            'mask': {'a': {'b': {}}},
        },
        {
            'fields': 'a(b,c)',
            'mask': {'a': {'b': {}, 'c': {}}},
        },
        {
            'fields': 'a(b,c/d)',
            'mask': {'a': {'b': {}, 'c': {'d': {}}}},
        },
        {
            'fields': 'z,a(b,c/d)',
            'mask': {'a': {'b': {}, 'c': {'d': {}}}, 'z': {}},
        },
        {
            'fields': 'a(b,c/d),z',
            'mask': {'a': {'b': {}, 'c': {'d': {}}}, 'z': {}},
        },
        {
            'fields': 'a(b,c/d(x,y,z))',
            'mask': {'a': {'b': {}, 'c': {'d': {'x': {}, 'y': {}, 'z': {}}}}},
        },
        {
            'fields': 'a(b,c/d(x,y,z),abc(xyz/z(a)))',
            'mask': {'a': {'b': {}, 'c': {'d': {'x': {}, 'y': {}, 'z': {}}, 'abc': {'xyz': {'z': {'a': {}}}}}}},
        },
        {
            'fields': 'a(b,c/d(x,y,z)),abc(xyz/z(a))',
            'mask': {'a': {'b': {}, 'c': {'d': {'x': {}, 'y': {}, 'z': {}}}}, 'abc': {'xyz': {'z': {'a': {}}}}},
        },
    ]

    for test in tests:
        error_msg = 'Failed to compile fields {}'.format(test['fields'])
        try:
            expect(test['mask']) == parsing.parse_fields(test['fields'])
        except Exception as e:
            logging.exception(e)
            raise e
