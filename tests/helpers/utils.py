from sys import version_info
import io
import hestia.api

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

try:
    from unittest.mock import patch
    from unittest.mock import MagicMock
except ImportError:
    from mock import patch
    from mock import MagicMock
    from mock import mock_open


def settings_from_string(settings):
    my_mock = MagicMock()

    if version_info.major == 2:
        with patch('__builtin__.open', return_value=io.BytesIO(settings)):
            return hestia.api.load_configuration()
    else:
        with patch('builtins.open', my_mock):
            manager = my_mock.return_value.__enter__.return_value
            manager.read.return_value = settings
            return hestia.api.load_configuration()