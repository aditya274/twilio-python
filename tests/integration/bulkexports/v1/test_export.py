# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from tests import IntegrationTestCase
from tests.holodeck import Request
from twilio.base.exceptions import TwilioException
from twilio.http.response import Response


class ExportTestCase(IntegrationTestCase):

    def test_fetch_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.bulkexports.v1.exports("resource_type").fetch()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://bulkexports.twilio.com/v1/Exports/resource_type',
        ))

    def test_fetch_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "resource_type": "Calls",
                "url": "https://bulkexports.twilio.com/v1/Exports/Calls",
                "links": {
                    "days": "https://bulkexports.twilio.com/v1/Exports/Calls/Days"
                }
            }
            '''
        ))

        actual = self.client.bulkexports.v1.exports("resource_type").fetch()

        self.assertIsNotNone(actual)
