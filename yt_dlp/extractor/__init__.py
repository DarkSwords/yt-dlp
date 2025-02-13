import contextlib
import os

from ..utils import load_plugins

_LAZY_LOADER = False
if not os.environ.get('YTDLP_NO_LAZY_EXTRACTORS'):
    with contextlib.suppress(ImportError):
        from .lazy_extractors import *  # noqa: F403
        from .lazy_extractors import _ALL_CLASSES
        _LAZY_LOADER = True

if not _LAZY_LOADER:
    from .extractors import *  # noqa: F403
    _ALL_CLASSES = [  # noqa: F811
        klass
        for name, klass in globals().items()
        if name.endswith('IE') and name != 'GenericIE'
    ]
    _ALL_CLASSES.append(GenericIE)  # noqa: F405

_PLUGIN_CLASSES = load_plugins('extractor', 'IE', globals())
_ALL_CLASSES = list(_PLUGIN_CLASSES.values()) + _ALL_CLASSES


def gen_extractor_classes():
    """ Return a list of supported extractors.
    The order does matter; the first extractor matched is the one handling the URL.
    """
    return _ALL_CLASSES


def gen_extractors():
    """ Return a list of an instance of every supported extractor.
    The order does matter; the first extractor matched is the one handling the URL.
    """
    return [klass() for klass in gen_extractor_classes()]


def list_extractors(age_limit):
    """Return a list of extractors that are suitable for the given age, sorted by extractor name"""
    return sorted(filter(
        lambda ie: ie.is_suitable(age_limit),
        gen_extractors()), key=lambda ie: ie.IE_NAME.lower())


def get_info_extractor(ie_name):
    """Returns the info extractor class with the given ie_name"""
    return globals()[ie_name + 'IE']
