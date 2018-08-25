__project__ = 'jsonmask'
__version__ = '0.0.0'

VERSION = "{0} v{1}".format(__project__, __version__)

from .mask import apply_json_mask, should_include_variable
from .parsing import parse_fields
