import sys

from .parsing import parse_fields


if sys.version_info[0] == 2:
    # pylint: disable=E0602
    string_types = (basestring,)
else:
    string_types = (str,)


def apply_json_mask(data, json_mask, is_negated=False, depth=1, max_depth=None):
    """Take a data structure and compiled JSON mask, and remove unwanted data.

    :data:          The Python dictionary you want to prune
    :json_mask:     The compiled jsonmask indicating which data to keep
                    and which to discard
    :is_negated:    If True, membership in the json_mask indicates removal
                    instead of inclusion
    :depth:         Recursion flag to maintain progress toward `max_depth`
    :max_depth:     Integer that, if supplied, sets a maximum depth on the
                    supplied `json_mask`

    :Returns:       dict

    """

    if max_depth and depth >= max_depth:
        raise ValueError('Too much nested data!')

    if isinstance(json_mask, string_types):
        json_mask = parse_fields(json_mask)

    allowed_data = {}
    for key, subdata in data.items():

        if should_include_variable(key, json_mask, is_negated=is_negated):

            # Terminal data
            if not isinstance(subdata, dict):
                allowed_data[key] = subdata
                continue

            next_json_mask = json_mask.get(key, {})

            # Dead ends in the mask indicate that want
            # everything nested below this
            if not next_json_mask:
                allowed_data[key] = subdata
                continue

            allowed_data.setdefault(key, {})
            allowed_data[key].update(
                apply_json_mask(
                    subdata,
                    next_json_mask,
                    is_negated=is_negated,
                    depth=depth + 1,
                    max_depth=max_depth,
                ),
            )

    return allowed_data


def is_structure_wildcard(structure):
    return len(structure) == 1 and list(structure.keys())[0] == '*'


def should_include_variable(path, structure, is_negated=False):
    """Determine inclusion of variable at path given parsed jsonmask.

    :path:          Something like "teacher.classes.students"
    :structure:     Nested structure whose keys may correlate
                    with the dotted path's tokens
    :is_negated:    If True, represents `?excludes` instead of `?fields`

    :returns:       bool
    """

    if not structure:
        return True

    return (
        do_fields_allow(path, structure)
        if not is_negated else
        not do_excludes_forbid(path, structure)
    )


def do_fields_allow(path, structure):
    path = path.split('.')
    struct = structure.copy()
    is_allowed = True

    for key in path:

        if not is_allowed:
            break

        is_wildcard = is_structure_wildcard(struct)

        if not is_wildcard and struct and key not in struct:
            is_allowed = False
        else:
            if is_wildcard:
                struct = struct['*']
            else:
                struct = struct.get(key, {})

    return is_allowed


def do_excludes_forbid(path, structure):
    path = path.split('.')
    struct = structure.copy()
    is_forbidden = True

    for index, key in enumerate(path, start=1):

        if not is_forbidden:
            break

        is_wildcard = is_structure_wildcard(struct)

        if not is_wildcard and struct and key not in struct:
            is_forbidden = False
        else:
            if is_wildcard:
                struct = struct['*']
            else:
                struct = struct.get(key, {})

        # Only on the last pass of the loop, take a gander and what
        # came next. If we're defining excluded sub-fields of this attribute
        # then we obviously want some other fields of this attribute, and
        # thus we want this attribute
        if index == len(path):
            if struct:
                return bool(is_structure_wildcard(struct))

    return is_forbidden
