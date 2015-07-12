from hestia.api import HestiaApi
import unittest
import httpretty

try:
    from unittest.mock import patch
    from unittest.mock import MagicMock
except ImportError:
    from mock import patch
    from mock import MagicMock

from helpers.utils import settings_from_string


class TestRecordSolarRiverInverterReading(unittest.TestCase):
    def setUp(self):
        config_file = """
[Remote]
url: https://test.hestia.io
username: username
password: password

[Photovoltaic]
installation_code: my_installation
        """
        settings = settings_from_string(config_file)
        self.api = HestiaApi(settings)

    @httpretty.activate
    def test_source_address(self):
        httpretty.register_uri(httpretty.POST,
                               "https://test.hestia.io/photovoltaic/my_installation/inverter/solar_river/readings",
                               status=202,
                               content_type="application/json")

        fake = MagicMock(date_taken=12345)
        self.api.record_solar_river_reading(fake)

        assert httpretty.last_request().method == "POST"
        assert httpretty.last_request().body.__len__() == 139
        assert httpretty.last_request().headers['content-type'] == 'application/json'


class TestRecordEmonReading(unittest.TestCase):
    def setUp(self):
        config_file = """
[Remote]
url: https://test.hestia.io
username: username
password: password

[Emon]
property_code: my_property
        """
        settings = settings_from_string(config_file)
        self.api = HestiaApi(settings)

    @httpretty.activate
    def test_source_address(self):
        httpretty.register_uri(httpretty.POST, "https://test.hestia.io/property/my_property/emon/readings",
                               status=202,
                               content_type="")

        mock_time = MagicMock(return_value=1436377530)
        with patch('time.time', mock_time):
            self.api.record_emon([[123, 10, 345, 0, 0], [345, 10, 123, 0, 0]])

        assert httpretty.last_request().method == "POST"
        assert httpretty.last_request().body == b"data=[[123,10,345,0,0],[345,10,123,0,0]]&sentat=1436377530"
        assert httpretty.last_request().headers['content-type'] == 'application/x-www-form-urlencoded'