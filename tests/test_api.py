from hestia.api import HestiaApi
import unittest
import httpretty

try:
    from unittest.mock import patch
    from unittest.mock import MagicMock
except ImportError:
    from mock import patch
    from mock import MagicMock


class TestRecordSolarRiverInverterReading(unittest.TestCase):
    def setUp(self):
        self.api = HestiaApi(dict(username='username', password='password'))

    @httpretty.activate
    def test_source_address(self):
        httpretty.register_uri(httpretty.POST,
                               "https://www.hestia.io/photovoltaic/my_installation/inverter/solar_river/readings",
                               status=202,
                               content_type="application/json")

        fake = MagicMock(date_taken=12345)
        self.api.record_solar_river_reading('my_installation', fake)

        assert httpretty.last_request().method == "POST"
        assert httpretty.last_request().body.__len__() == 139
        assert httpretty.last_request().headers['content-type'] == 'application/json'
        assert httpretty.last_request().headers['user-agent'] == 'Hestia Python API/%s' % HestiaApi.__version__


class TestRecordEmonReading(unittest.TestCase):
    def setUp(self):
        self.api = HestiaApi(dict(username='username', password='password'))

    @httpretty.activate
    def test_source_address(self):
        httpretty.register_uri(httpretty.POST, "https://www.hestia.io/property/my_property/emon/readings",
                               status=202,
                               content_type="")

        mock_time = MagicMock(return_value=1436377530)
        with patch('time.time', mock_time):
            self.api.record_emon('my_property', [[123, 10, 345, 0, 0], [345, 10, 123, 0, 0]])

        assert httpretty.last_request().method == "POST"
        assert httpretty.last_request().body == b"data=[[123,10,345,0,0],[345,10,123,0,0]]&sentat=1436377530"
        assert httpretty.last_request().headers['content-type'] == 'application/x-www-form-urlencoded'
        assert httpretty.last_request().headers['user-agent'] == 'Hestia Python API/%s' % HestiaApi.__version__


class TestStatus(unittest.TestCase):
    def setUp(self):
        self.api = HestiaApi(dict(username='username', password='password'))

    @httpretty.activate
    def test_source_address(self):
        httpretty.register_uri(httpretty.GET, "https://www.hestia.io/status",
                               status=200,
                               content_type="application/json")

        response = self.api.status()

        assert response == 200
        assert httpretty.last_request().method == "GET"
        assert httpretty.last_request().headers['user-agent'] == 'Hestia Python API/%s' % HestiaApi.__version__
