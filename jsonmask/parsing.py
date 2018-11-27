from __future__ import unicode_literals


TERMINALS = ['(', ')', ',', '/']


def maybe_add_word(name, tokens):
    if name:
        tokens.append(name)
        name = ''
    return name, tokens


def tokenize_partial_response(text):
    tokens = []
    name = ''

    if not text:
        return tokens

    for ch in text:
        if ch in TERMINALS:
            name, tokens = maybe_add_word(name, tokens)
            tokens.append(ch)

        else:
            name += ch

    name, tokens = maybe_add_word(name, tokens)
    return tokens


def parse_partial_response(tokens):
    return _parse_partial_response(tokens, {}, [])


def _parse_partial_response(tokens, parent, stack):
    parent = parent.copy()
    props = {}

    while True:
        if not tokens:
            return parent

        token = tokens.pop(0)
        if token not in TERMINALS:

            stack.append(token)
            resp = _parse_partial_response(
                tokens, props.get(token, {}), stack,
            )
            props[token] = resp
            stack.pop()

        elif token == ',':
            return props

        elif token == '/':
            stack.append(token)
            continue

        elif token == '(':
            stack.append(token)
            continue

        elif token == ')':
            return props

        parent.update(props)

        if stack and stack[-1] in ['/']:
            stack.pop()
            return parent

    return parent


def parse_fields(text):
    """Turn a string jsonmask into a Python dictionary representing the desired data pruning.

    You will likely want to call ``jsonmask.mask.apply_json_mask``.

    :text:      Plain text value representing desired structure, e.g., `a,b/c`

    :returns:   dict
    """
    if not text:
        return None

    return parse_partial_response(
        tokens=tokenize_partial_response(text),
    )
