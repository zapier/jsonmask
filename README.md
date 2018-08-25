Unix: [![Unix Build Status](https://img.shields.io/travis/craiglabenz/jsonmask/master.svg)](https://travis-ci.org/craiglabenz/jsonmask) Windows: [![Windows Build Status](https://img.shields.io/appveyor/ci/craiglabenz/jsonmask/master.svg)](https://ci.appveyor.com/project/craiglabenz/jsonmask)<br>Metrics: [![Coverage Status](https://img.shields.io/coveralls/craiglabenz/jsonmask/master.svg)](https://coveralls.io/r/craiglabenz/jsonmask) [![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/craiglabenz/jsonmask.svg)](https://scrutinizer-ci.com/g/craiglabenz/jsonmask/?branch=master)<br>Usage: [![PyPI Version](https://img.shields.io/pypi/v/jsonmask.svg)](https://pypi.org/project/jsonmask)

# Overview

Implements [Google Partial Response](https://developers.google.com/discovery/v1/performance#partial-response) / [`json-mask`](https://github.com/nemtsov/json-mask) in Python.

## Requirements

* Python 2.7
* Python 3.6+

## Installation

Install jsonmask with pip:

```sh
$ pip install jsonmask
```

or directly from the source code:

```sh
$ git clone https://github.com/zapier/jsonmask.git
$ cd jsonmask
$ python setup.py install
```

# Usage

After installation, the package can imported:

```sh
$ python
>>> import jsonmask
>>> jsonmask.__version__
```

To prune dictionaries:

```py
import jsonmask
mask = jsonmask.parse_fields('a,b(c,d)')
jsonmask.apply_json_mask(
    {
        'a': {
            'nested_within_a': True,
        },
        'b' {
            'c': True,
            'd': {'Will get included?': 'Yes'},
            'e': 'Tough luck here',
        },
        'c': 'Definitely hopeless',
    },
    mask,
)

>>> {
        'a': {
            'nested_within_a': True,
        },
        'b' {
            'c': True,
            'd': {'Will get included?': 'Yes'},
        },
    },
```
