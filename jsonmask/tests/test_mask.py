"""Sample unit test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison
import logging

from jsonmask import mask


def test_apply_json_mask():

    print('omg')

    ORIGINAL = 'original'
    EMPTY = 'empty'

    tests = [
        # (data, mask, result, result_when_mask_negated,)
        # 0
        ({'a': 1}, 'a', ORIGINAL, EMPTY,),
        ({'a': 1}, 'b', EMPTY, ORIGINAL,),
        ({'a': 1}, 'a/b', ORIGINAL, ORIGINAL,),  # Drilling into terminal-values is a no-op
        ({'a': {'b': 1}}, 'a', ORIGINAL, EMPTY,),
        ({'a': {'b': 1}}, 'b', EMPTY, ORIGINAL,),
        # 5
        ({'a': {'b': 1}}, 'a/b', ORIGINAL, {'a': {}},),
        ({'a': {'b': 1}}, 'a/c', {'a': {}}, ORIGINAL,),
        ({'a': {'b': 1}, 'b': {'asdf': 2}}, 'a,b/c', {'a': {'b': 1}, 'b': {}}, {'b': {'asdf': 2}},),
        ({'a': {'b': 1}, 'b': {'asdf': 2}}, 'a,b/asdf', ORIGINAL, {'b': {}},),
        ({'a': {'b': 1}, 'b': {'asdf': 2}}, 'a,c/c', {'a': {'b': 1}}, {'b': {'asdf': 2}},),
    ]

    for index, (data, _mask, expected_result, expected_result_when_negated,) in enumerate(tests, start=1):

        if expected_result == ORIGINAL:
            expected_result = data.copy()

        if expected_result == EMPTY:
            expected_result = {}

        if expected_result_when_negated == ORIGINAL:
            expected_result_when_negated = data.copy()

        if expected_result_when_negated == EMPTY:
            expected_result_when_negated = {}

        try:
            pruned_data = mask.apply_json_mask(data, _mask)
            assert pruned_data == expected_result
        except Exception as e:
            logging.exception('Encountered %s on include test %s', type(e).__name__, index)
            raise e

        try:
            pruned_data = mask.apply_json_mask(data, _mask, is_negated=True)
            assert pruned_data == expected_result_when_negated
        except Exception as e:
            logging.exception('Encountered %s on exclude test %s', type(e).__name__, index)
            raise e


def test_inclusion_resolver():
    tests = [
        # (
        #   path, includes/exclude,
        #   expected_include_result, expected_exclude_result,
        # )
        # 0
        ('a', {}, True, True,),
        ('a.b', {}, True, True,),
        ('a', {'a': {}}, True, False,),
        ('a.b', {'a': {}}, True, False,),
        ('a.b', {'a': {'c': {}}}, False, True,),
        # 5
        ('a', {'a': {'b': {}}}, True, True,),
        ('a.b', {'a': {'b': {}}}, True, False,),
        ('a', {'a': {'*': {}}}, True, False,),
        ('a.b', {'a': {'*': {}}}, True, False,),
        ('a.b.c', {'a': {'*': {}}}, True, False,),
        # 10
        ('a.b.c', {'a': {'*': {'d': {}}}}, False, True,),
        ('a.b.c', {'b': {}}, False, True,),
        ('a.b.c', {'a': {'b': {'d': {}}}}, False, True,),
        ('a.b.d', {'a': {'b': {'d': {}}}}, True, False,),
    ]

    for index, (path, structure, result_as_include, result_as_exclude,) in enumerate(tests, start=1):

        wrong_include_value = 'False' if result_as_include else 'True'
        error_msg = 'Incorrectly returned {} on include test for path `{}` on test {}'.format(
            wrong_include_value,
            path,
            index,
        )
        assert mask.should_include_variable(path, structure) == result_as_include, error_msg

        wrong_exclude_value = 'False' if result_as_exclude else 'True'
        error_msg = 'Incorrectly returned {} on exclude test for path `{}` on test {}'.format(
            wrong_exclude_value,
            path,
            index,
        )
        assert mask.should_include_variable(path, structure, is_negated=True) == result_as_exclude, error_msg
